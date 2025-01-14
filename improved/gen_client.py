import socket
import rsa
import pickle

# Client class
class Client:
    def __init__(self, server_host='localhost', server_port=12345):
        self.server_host = server_host
        self.server_port = server_port

        # Generate RSA keys for the client
        self.client_public_key, self.client_private_key = rsa.newkeys(512)

        # Connect to the server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_host, self.server_port))

        # Step 1: Receive the server's public key
        self.server_public_key = pickle.loads(self.client_socket.recv(4096))

        # Step 2: Send the client's public key to the server
        self.client_socket.send(pickle.dumps(self.client_public_key))

    def send_message(self, message):
        # Encrypt the message with the server's public key
        encrypted_message = rsa.encrypt(message.encode('utf-8'), self.server_public_key)
        self.client_socket.send(encrypted_message)

    def receive_message(self):
        while True:
            encrypted_message = self.client_socket.recv(4096)
            if not encrypted_message:
                break
            decrypted_message = rsa.decrypt(encrypted_message, self.client_private_key).decode('utf-8')
            print(f"Received message: {decrypted_message}")

    def pair_with(self, recipient_id):
        # Pair with another client by sending a pairing request to the server
        self.send_message(f"PAIR {recipient_id}")
    
    def start_receiving(self):
        # Start a thread to listen for incoming messages
        threading.Thread(target=self.receive_message, daemon=True).start()

    def start(self):
        # Start receiving messages
        self.start_receiving()
        
        # Example of sending a message
        while True:
            message = input("Enter message: ")
            self.send_message(message)


# Example usage for client 1
client1 = Client()
client1.pair_with(2)  # Pair client 1 with client 2 (assuming client 2 is running)
client1.start()
