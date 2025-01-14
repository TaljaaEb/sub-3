# This was created using Ai
import socket
import rsa
import threading

# Generate RSA keys for server
(public_key, private_key) = rsa.newkeys(512)

# Store clients' public keys in a dictionary (client_id -> public_key)
clients_public_keys = {}

def handle_client(client_socket, client_address):
    global clients_public_keys

    # Receive the client's public key
    client_public_key_data = client_socket.recv(512)
    client_public_key = rsa.PublicKey.load_pkcs1(client_public_key_data)
    clients_public_keys[client_address] = client_public_key

    try:
        while True:
            # Receive encrypted message from the client
            encrypted_msg = client_socket.recv(1024)

            if not encrypted_msg:
                break

            # Decrypt the message with server's private key
            decrypted_msg = rsa.decrypt(encrypted_msg, private_key).decode('utf-8')
            print(f"Received message: {decrypted_msg} from {client_address}")

            # Example of re-encrypting and forwarding the message to another client (can be a paired client in real scenario)
            target_address = list(clients_public_keys.keys())[0]  # Just as an example
            target_client_socket = client_socket  # Simulate paired client socket

            # Encrypt the message before sending it to the target client
            encrypted_msg_to_send = rsa.encrypt(decrypted_msg.encode('utf-8'), clients_public_keys[target_address])

            # Send the encrypted message to the target client
            target_client_socket.send(encrypted_msg_to_send)

    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()

def start_server(host='127.0.0.1', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()
