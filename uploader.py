import requests

def upload_to_bale(file_path, bot_token, chat_id):
    url = f"https://tapi.bale.ai/bot{bot_token}/sendDocument"

    with open(file_path, "rb") as f:
        files = {
            "document": f
        }
        data = {
            "chat_id": chat_id
        }

        r = requests.post(url, data=data, files=files)
        if r.status_code != 200:
            raise Exception(f"Bale upload failed: {r.text}")