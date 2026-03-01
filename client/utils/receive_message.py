import json
def receive_message(client,oponent_queue):
    buffer = ""
    while True:
        try:
            chunk = client.recv(1024).decode()
            if not chunk:
                print("Connection closed by the server.")
                return None
            buffer += chunk
            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)
                received_state = json.loads(message)
                oponent_queue.put(received_state)
        except Exception as e:
            print(f"Error receiving message: {e}")
            return None