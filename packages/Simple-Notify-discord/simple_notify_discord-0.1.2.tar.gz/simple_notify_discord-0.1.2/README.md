# Simple-Notify-Discord

https://pypi.org/project/Simple-Notify-discord/

**Simple-Notify-Discord** allows you to easily send a message to a Discord channel via a webhook.  
You can use it to alert when a process is finished, when an error occurs, or for any other context where you need simple notifications.

---

## Installation

```bash
pip install Simple-Notify-discord
```

---

## Usage

First, import the `SimpleNotifyDiscord` class:

```python
from simple_notify_discord import SimpleNotifyDiscord

notifier = SimpleNotifyDiscord()
notifier.notify_discord("✅ Your task is complete!", mention=True)
```

If you set `mention=True`, the user ID will be mentioned at the beginning of the message.

---

## How It Works

The class `SimpleNotifyDiscord` sends a message to your Discord server through a webhook URL.

Here's the internal structure:

```python
import requests

class SimpleNotifyDiscord:
    def __init__(self):
        self.webhook_url = "your webhook URL here"
        self.user_id = "your Discord user ID here"

    def notify_discord(self, message="Hey, this is a notification from Notify", mention=False):
        if mention:
            message = f"<@{self.user_id}> {message}"
        data = {"content": message}
        response = requests.post(self.webhook_url, json=data)
        if response.status_code == 204:
            print("✅ Notification Discord sent successfully")
        else:
            print(f"❌ Error: {response.text}")
```

---

## Setup

### 1. Create a Discord Webhook

- Go to your Discord server.
- Click **Server Settings** → **Integrations** → **Webhooks**.
- Click **New Webhook**.
- Choose the channel where you want notifications.
- Copy the webhook URL and paste it into your `SimpleNotifyDiscord` class (`self.webhook_url`).

### 2. Find your Discord User ID

If you want the bot to mention you:
- Enable **Developer Mode** in Discord (Settings → Advanced → Developer Mode).
- Right-click your profile → **Copy ID**.
- Paste this ID into your `SimpleNotifyDiscord` class (`self.user_id`).

> If `mention=True`, your notification will automatically tag you.

---

## Repository

The project is open-source and available here:  
[https://github.com/CogalTek/SimpleNotifyDiscord](https://github.com/CogalTek/SimpleNotifyDiscord)

---

## License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.
