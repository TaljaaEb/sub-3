
import socket
import rsa
import pickle
import threading
import time
import hashlib, errno

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IP = s.getsockname()[0]
    s.close()
    return IP

def get_username():
    USER = os.getlogin()
    return USER

def hashing(ctext):
    obj = hashlib.sha1()
    obj.update(bytes(ctext, 'utf-8'))
    return obj.hexdigest()

ip = get_ip()
user = get_username()

ctext = hashing(ip + user)
print(ctext)
print("\n")

# Client class
class Client:
    def __init__(self, server_host='remotehost', server_port=443):
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
            print(f"{decrypted_message}")
#            print(f"Received message: {decrypted_message}")

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
#        while True:
#            input("?")
#            message = input("Enter message: ")
#            self.send_message(ctext)
            #time.sleep(5)
            #message = ip + user
#            try: 
#                self.send_message(ctext)
#                break
#            except IOError as e: 
#                if e.errno == errno.EPIPE: 
#                    print(e)
#                    pass
                    # Handling of the error 
        while True:
            message = input("?")
            self.send_message(ctext)
            message = input("?")
            self.send_message("CTRU")

# Example usage for client 1
client1 = Client()
client1.pair_with(2)  # Pair client 1 with client 2 (assuming client 2 is running)
client1.start()
