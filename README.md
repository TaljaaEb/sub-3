# sub-3

How the System Works
Server:

The server generates an RSA key pair.
It listens for incoming connections from clients.
When a client connects, the server receives the client's public key and stores it.
The server decrypts incoming messages from clients using its private key.
It then re-encrypts the message using the target client's public key and sends it to the intended recipient.
Client:

Each client generates its RSA key pair.
The client sends its public key to the server.
When the client sends a message, it encrypts it using its own public key.
The client waits for the server's response, which is encrypted. The client then decrypts it with its private key.
How to Test the System
Run the server script.
Run two instances of the client script.
In each client, send a message, and the server will relay it back to the other client.
Improvements
Implement pairing logic between clients, where the server forwards messages only to the intended recipient.
Use a more robust system for managing client connections, like implementing a queue or mapping system for the paired clients.
