import requests

class Simple_Notify_Discord:
    def __init__(self):
        self.webhook_url = "bot url"
        self.user_id = "user_id"

    def notify_discord(self, message = "Hey this is a notification from Notify", mention = False):
        if mention:
            message = self.user_id + message
        data = {
            "content": message
        }
        response = requests.post(self.webhook_url, json=data)
        if response.status_code == 204:
            print("✅ Notification Discord send with success")
        else:
            print("❌ Error:", response.text)