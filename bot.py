import requests
import threading
import time
import os
import signal
import tkinter as tk
from tkinter import messagebox
import discord
import asyncio

# Global variables
webhook_url = ""
message = ""
spam_count = 0
target_user_id = ""
delay = 0
bot_token = ""

# Discord client
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

# Signal handler
def handle_exit_signal(sig, frame):
    print("\n[!] Exiting...")
    exit(0)

signal.signal(signal.SIGINT, handle_exit_signal)

# Server spammer
def send(webhook_url, message):
    global spam_count
    while spam_count > 0:
        try:
            response = requests.post(
                webhook_url,
                json={"content": message},
                timeout=10
            )
            if response.status_code == 204:
                print("[+] Message sent")
            spam_count -= 1
        except Exception:
            pass
        time.sleep(delay / 1000)

# Discord bot logic
@client.event
async def on_ready():
    print(f"[+] Logged in as {client.user}")
    try:
        user = await client.fetch_user(int(target_user_id))
        for i in range(spam_count):
            await user.send(f"{message} ({i+1})")
            print(f"[+] Sent message {i+1}")
            await asyncio.sleep(delay / 1000)
    except Exception as e:
        print(f"[!] Error: {e}")
    await client.close()

# GUI Components
def main_menu():
    window = tk.Tk()
    window.title("Main Menu")
    window.geometry("520x400")
    window.configure(bg="#40E0D0")

    def open_dm_spammer():
        window.destroy()
        dm_spammer_gui()

    def open_server_spammer():
        window.destroy()
        server_spammer_gui()

    tk.Label(window, text="Spammer Control Panel", fg="#ff3333", bg="#40E0D0",
             font=("Helvetica Neue", 18, "bold")).pack(pady=15)
    tk.Button(window, text="DM Spammer", font=("Helvetica Neue", 12, "bold"),
              bg="red", fg="white", command=open_dm_spammer).pack(pady=20)
    tk.Button(window, text="Server Spammer", font=("Helvetica Neue", 12, "bold"),
              bg="red", fg="white", command=open_server_spammer).pack(pady=10)
    window.mainloop()

def dm_spammer_gui():
    window = tk.Tk()
    window.title("DM Spammer")
    window.geometry("520x600")
    window.configure(bg="#40E0D0")

    style = {"bg": "#40E0D0", "fg": "#ffffff", "font": ("Helvetica Neue", 12)}

    tk.Label(window, text="DM Spammer", fg="#ff3333", bg="#40E0D0",
             font=("Helvetica Neue", 18, "bold")).pack(pady=15)

    entries = {}

    def add_field(label_text, key):
        tk.Label(window, text=label_text, **style).pack(pady=(10, 0))
        entry = tk.Entry(window, font=("Helvetica Neue", 12), bg="#1a1a1a", fg="white")
        entry.pack(pady=5, ipadx=5, ipady=4)
        entries[key] = entry

    add_field("Bot Token:", "token")
    add_field("Target User ID:", "user_id")
    add_field("Message:", "message")
    add_field("Number of Messages:", "count")
    add_field("Delay Between Messages (ms):", "delay")

    login_status_label = tk.Label(window, text="Not logged in", bg="#40E0D0", fg="red", font=("Helvetica Neue", 12))
    login_status_label.pack(pady=10)

    def set_settings():
        global target_user_id, message, spam_count, delay, bot_token
        bot_token = entries["token"].get()
        target_user_id = entries["user_id"].get()
        message = entries["message"].get()
        try:
            spam_count = int(entries["count"].get())
        except ValueError:
            spam_count = 0
        try:
            delay = int(entries["delay"].get())
        except ValueError:
            delay = 0
        print("[+] DM settings updated")

    def start_dm_spamming():
        set_settings()
        threading.Thread(target=lambda: asyncio.run(client.start(bot_token))).start()
        login_status_label.config(text="Logging in...", fg="orange")

    tk.Button(window, text="Set Settings", font=("Helvetica Neue", 12, "bold"),
              bg="#ff3333", fg="white", command=set_settings).pack(pady=20)
    tk.Button(window, text="Start DM Spamming", font=("Helvetica Neue", 12, "bold"),
              bg="red", fg="white", command=start_dm_spamming).pack(pady=10)
    tk.Button(window, text="Back to Main Menu", font=("Helvetica Neue", 12, "bold"),
              bg="red", fg="white", command=lambda: [window.destroy(), main_menu()]).pack(pady=10)

    window.mainloop()

def server_spammer_gui():
    window = tk.Tk()
    window.title("Server Spammer")
    window.geometry("520x600")
    window.configure(bg="#40E0D0")

    style = {"bg": "#40E0D0", "fg": "#ffffff", "font": ("Helvetica Neue", 12)}
    entries = {}

    tk.Label(window, text="Server Spammer", fg="#ff3333", bg="#40E0D0",
             font=("Helvetica Neue", 18, "bold")).pack(pady=15)

    def add_field(label_text, key):
        tk.Label(window, text=label_text, **style).pack(pady=(10, 0))
        entry = tk.Entry(window, font=("Helvetica Neue", 12), bg="#1a1a1a", fg="white")
        entry.pack(pady=5, ipadx=5, ipady=4)
        entries[key] = entry

    add_field("Webhook URL:", "url")
    add_field("Message:", "message")
    add_field("Number of Messages:", "count")
    add_field("Delay Between Messages (ms):", "delay")

    def set_settings():
        global webhook_url, message, spam_count, delay
        webhook_url = entries["url"].get()
        message = entries["message"].get()
        try:
            spam_count = int(entries["count"].get())
        except ValueError:
            spam_count = 0
        try:
            delay = int(entries["delay"].get())
        except ValueError:
            delay = 0
        print("[+] Server settings updated")

    def start_server_spamming():
        set_settings()
        threading.Thread(target=send, args=(webhook_url, message)).start()

    tk.Button(window, text="Set Settings", font=("Helvetica Neue", 12, "bold"),
              bg="#ff3333", fg="white", command=set_settings).pack(pady=20)
    tk.Button(window, text="Start Server Spamming", font=("Helvetica Neue", 12, "bold"),
              bg="red", fg="white", command=start_server_spamming).pack(pady=10)
    tk.Button(window, text="Back to Main Menu", font=("Helvetica Neue", 12, "bold"),
              bg="red", fg="white", command=lambda: [window.destroy(), main_menu()]).pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    main_menu()

