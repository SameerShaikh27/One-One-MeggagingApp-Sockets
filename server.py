import socket
import threading

HOST = "127.0.0.1"
PORT = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
names = []


# BROADCAST FUNCTION
# This functions will sends the message to all the client
def broadcast(message):
    for client in clients:
        client.send(message)


# HANDLE FUNCTION
# After accepting the new connection this function will handle the conversation and connection between client and server
def handle(client):
    while True:
        try:
            # Here we are trying to receive a message from a client
            message = client.recv(1024)
            # Using "index" method to find out that which name belongs to which client.
            print(f"{names[clients.index(client)]} says {message}")
            # Broadcasting a message to all the clients connected
            broadcast(message)

        except :
            # If the content in the "try" shows error then we will remove client from the clients and names list
            # First, we are trying to find out that in which position is this current client in.
            index = clients.index(client)
            # Removing the client
            clients.remove(client)
            client.close()

            # Trying to find out the index number of the current client name in names list
            name = names[index]
            # Removing the name
            names.remove(name)
            break


# RECEIVE FUNCTION
# This function will accept the new connections (clients). It is going to listen to them again and again.
def receive():
    while True:
        # Accepting the new connection and IP Address
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Using "client.send" to send a message to ask for a name so that we know who we are connecting with.
        client.send("Name".encode("utf-8"))
        # With the help of "client.recv" we wil receive the name of the client.
        name = client.recv(1024)

        # After receiving the name of the client, we are appending it to the names empty list.
        names.append(name)
        # Appending the new client in the clients list
        clients.append(client)

        # Below code is just a server message, we will not send it to all the client
        print(f"Name of the client is {name}")

        # Here, we are sending a message to all the clients that are connected with the help of "broadcast" function.
        broadcast(f"{name} connected to the server!\n".encode('utf-8'))

        # Here, we are only sending a message to a client which got recently connected.
        client.send("Connected to the server".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server Running....")
receive()




