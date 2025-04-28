# Simple-Notify-discord

**Simple-Notify-discord** allows you to easily send a message to a Discord channel via a webhook.  
You can use it to alert when a process is finished, when an error occurs, or for any other context where you need simple notifications.

## Installation

*(Coming soon after publishing to PyPI)*

## Usage

First, set up the `Simple-Notify-discord` class:

```python
import requests

class Notify:
    def __init__(self):
        self.webhook_url = "your webhook URL here"
        self.user_id = "your Discord user ID here"

    def Simple_Notify_discord(self, message="Hey this is a notification from Notify", mention=False):
        if mention:
            message = self.user_id + message
        data = {
            "content": message
        }
        response = requests.post(self.webhook_url, json=data)
        if response.status_code == 204:
            print("✅ Notification Discord sent successfully")
        else:
            print("❌ Error:", response.text)
```

### Example

```python
notifier = Notify()
notifier.notify_discord("✅ Your task is complete!", mention=True)
```

If you set `mention=True`, the user ID will be mentioned at the beginning of the message.

---

## Setup

### 1. Create a Discord Webhook

- Go to your Discord server.
- Click on the **server settings** → **Integrations** → **Webhooks**.
- Click **New Webhook**.
- Choose the channel where the messages will be sent.
- Copy the webhook URL and paste it into your `Notify` class (`self.webhook_url`).

### 2. Find your Discord User ID

If you want the bot to mention you:
- Enable **Developer Mode** in Discord settings (Settings → Advanced → Developer Mode).
- Right-click on your profile and select **Copy ID**.
- Paste this ID into your `Notify` class (`self.user_id`).

---

## License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.
