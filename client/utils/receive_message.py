import json

def receive_message(client,oponent_queue):
    while True:
        try:
            message = client.recv(1024)
            received_state = json.loads(message.decode())
            oponent_queue.put(received_state)
        except Exception as e:
            print(f"Error receiving message: {e}")
            return None