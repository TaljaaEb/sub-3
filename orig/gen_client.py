# This was generated using Ai
import socket
import rsa

# Generate RSA keys for client
(public_key, private_key) = rsa.newkeys(512)

def connect_to_server(host='127.0.0.1', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Send the client's public key to the server
    client_socket.send(public_key.save_pkcs1())

    try:
        while True:
            message = input("Enter message to send: ")

            # Encrypt the message using server's public key
            encrypted_message = rsa.encrypt(message.encode('utf-8'), public_key)

            # Send the encrypted message to the server
            client_socket.send(encrypted_message)

            # Receive the response (encrypted) from the server
            encrypted_response = client_socket.recv(1024)

            # Decrypt the server's response using the client's private key
            decrypted_response = rsa.decrypt(encrypted_response, private_key).decode('utf-8')

            print(f"Received from server: {decrypted_response}")

    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    connect_to_server()
