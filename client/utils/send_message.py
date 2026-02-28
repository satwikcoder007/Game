import json
def send_message(client, message):
    try:
        message = json.dumps(message)
        client.send(message.encode())
    except Exception as e:
        print(f"Error sending message: {e}")