# CMP2204 Introduction to Computer Networks, Spring 2024, Term Project

## Service Announcer

The `Service_Announcer.py` script is used to broadcast the presence of a user on a local network. It sends out a broadcast message every 8 seconds with the user's username. The user can specify their username and the IP address for broadcasting. If no IP address is specified, it defaults to 'localhost'. It broadcasts the message on port 6000.

### Usage
First enter your username press enter and then enter the IP address of the network you want to broadcast to. If you want to broadcast to the local network, you can leave the IP address field empty and press enter.
```bash
python Service_Announcer.py
```

## Peer Discovery

The `Peer_Discovery.py` script is responsible for discovering other peers on the network. It listens for broadcast messages in port 6001 that are sent by the `Service_Announcer.py` script and updates a list of online peers accordingly. This list is stored in the `online_peers.txt` file.

### Usage
Enter the IP address of the network you want to discover peers from. If you want to discover peers from the local network, you can leave the IP address field empty and press enter.
```bash
python Peer_Discovery.py
```

## Chat Responder

The `Chat_Responder.py` script is a server-side script that handles incoming chat messages from clients. It supports both encrypted and unencrypted messages. For encrypted messages, it uses the Diffie-Hellman key exchange protocol to establish a shared secret key with the client. The script prints all the incoming messages and prints them. It also maintains a log of all received and sent messages in the `chat_history.txt` file.

### Usage
Run the code and the rest is automatic
```bash
python Chat_Responder.py
```

## Chat Initiator

The `Chat_Initiator.py` script is responsible for initiating a chat session with a peer. It sends a chat message to the server, which can be either encrypted or unencrypted. For encrypted messages, it uses the Diffie-Hellman key exchange protocol to establish a shared secret key with the server. It maintains a log of all received and sent messages in the `chat_history.txt` file.

### Usage
When you run the code, you will be prompted to enter one of the four options: Users, Chat, History or Exit. Enter 'Users' to see the list of online users; 'Chat' to start a chat session with a user by writing the user's username, selecting if you want a secure connection or not, if secure entering a number to encrypt and sending you message; 'History' to see the chat history and 'Exit' to exit the program.
```bash
python Chat_Initiator.py
```

## Running the Scripts
- Run and use the scripts in the following order:
  1. Run `Service_Announcer.py` to broadcast your presence on the network.
  2. Run `Peer_Discovery.py` to discover other peers on the network.
  3. Run `Chat_Responder.py` to start the chat server.
  4. Run `Chat_Initiator.py` to start a chat session with a peer.

### Known Limitations
Maximum of 5 users can be making TCP connections at the same time.