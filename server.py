import sys  # to access command line arguments
import socket   # to use sockets in our program
import bots    # to use the bot commands from another .py file
import threading    # to use threads

# Creates a socket using TCP/IP protocol
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

inputArg = sys.argv[1]
# Checks to see if we have received the correct amount of cl arguments
if str(inputArg) == '-h' or str(inputArg) == '--help':  # if program is called with -h or --help
    print("Command line argument should be a port-number")
    exit()

Port = int(sys.argv[1])     # Takes the first argument from command prompt as port number

serverSocket.bind(('192.168.0.99', Port))   # Binds to address

serverSocket.listen()   # Socker listens for new connections

clients = []    # List of connected clients
nicknames = []  # List of nicknames for the connected clients


def broadcast(message):  # Method to send a message to all connected clients
    check()     # Checks first if any clients have disconnected
    for client in clients:
        client.send(message)    # Sends message to all clients


def forward(sender, message):   # Method to send a message to all connected clients except the sender
    for client in clients:
        if client != sender:
            client.send(message)


def check():    # Method to check if any clients have disconnected
    for client in clients:
        try:
            client.send("CONN".encode())    # Sends a request for confirmation to all clients
            confirmation = client.recv(1024)    # We can ignore the reply, since it's just a confirmation
        except socket.error as e:   # Exception if we can't send or receive from a client
            index = clients.index(client)
            clients.remove(client)  # Removes client from list of connections
            client.close()      # Closes the client
            nickname = nicknames[index]
            nicknames.remove(nickname)  # Removes nickname from list
            print(f'\n({nickname} has left the chat!)')
            broadcast(f'\n({nickname} has left the chat!)'.encode())


def close_all():    # Method to close all remaining client connections
    for client in clients:
        client.close()


def kick(bot_name):     # Method to kick a bot by providing a nickname
    bot_name = bot_name.capitalize()
    if bot_name in nicknames:   # If the bot is connected
        index = nicknames.index(bot_name)
        client = clients[index]
        clients.remove(client)  # Remove from list of connections
        nicknames.remove(bot_name)
        client.send("\n(You have been kicked from the chat!)".encode())
        client.close()  # Close the client connection
        broadcast(f'\n({bot_name} was kicked from the chat!)'.encode())
        print(f'\n({bot_name} was kicked from the chat!)')
    else:   # If the bot isn't connected
        print(f"\nThere is no bot called {bot_name} in this chat")


def help():     # Method to print all valid commands
    print("When prompted for input, the following commands can be used:\n")
    print("r: Generate a random suggestion for the bots")
    print("i: Make your own suggestion to the bots through input")
    print("k: Kick a bot from the chat")
    print("q: Close the chat")
    print("h: Show this menu again")


serverSocket.settimeout(1.0)    # Timeout for accepting a connection


def acceptLoop():   # Loop that accepts new client connections while True
    while Accepting:
        try:
            client, address = serverSocket.accept()  # Accepts new connection
            client.send('NICK'.encode())    # Requests a nickname
            nickname = client.recv(1024).decode()   # Receives a nickname
            nicknames.append(nickname)  # Adds new client's nickname to list
            clients.append(client)  # Adds new client to list

            print(f'\n(New connection from {address}, {nickname} has joined the chat!)')
            broadcast(f'\n({nickname} has joined the chat!)'.encode())
        except socket.timeout as e:
            pass    # Nothing happens if we get a timeout


Running = True
Accepting = True
thread = threading.Thread(target=acceptLoop)    # Starts the 'acceptLoop' on a separate thread
thread.start()


def suggest(a):     # Method to suggest something to the clients
    suggestion = f'SUGG {a}'  # Start the suggestion with a keyword so clients recognize it as a request
    broadcast(f"\nThe host has suggested {a}ing".encode())  # Broadcast this round's suggestion

    client_no = 0   # counter variable, so we know which client we are currently handling
    for client in clients:  # For each connected client
        client.send(suggestion.encode())    # Sends the request to client
        client.settimeout(5.0)      # Sets a time limit of 5 seconds for the client to answer
        try:
            reply = client.recv(1024).decode()  # Fetches the reply
        except socket.timeout as e:     # Timeout from the socket
            reply = None

        if reply:   # If the client replies within 5 seconds
            print(reply)
            forward(client, reply.encode())  # Forwards the reply to all the other clients
            reply = None

        else:   # If the client doesn't reply within 5 seconds
            index = clients.index(client)
            client.close()  # Closes the client's connection
            clients.remove(client)  # Removes client from the list of connected clients
            nickname = nicknames[index]
            print(f'\n({nickname} was disconnected due to inactivity!)')
            broadcast(f'\n({nickname} was disconnected due to inactivity!)'.encode())
            nicknames.remove(nickname)  # Removes the client's nickname from the list

        client_no = client_no + 1   # Add 1 to the counter variable, and move on to the next client


# The main Program starts here

print("\nWelcome to Thea\'s bots!")
help()  # The help() method prints out a list of usable commands
print("\nWaiting for at least 2 people to join the room...")

round_no = 1    # Counter variable for number of suggestion-rounds

while Running:  # Continues to start new rounds until either Running = False or we use break
    #   Looking for new connections
    if len(clients) > 1:    # We need at least 2 connections before starting a round

        u_input = input("\nEnter a command or type [h] for help: ")

        if round_no > 1:    # Every round after the first, we call our check() method
            check()  # Checks to see if any clients have disconnected since last round

            if len(clients) < 2:    # If there is only one person left, the chat closes automatically
                print("\nNot enough people left! Closing the chat room...")
                break

        if u_input == "r":  # User wants to send a random suggestion to the clients
            action = bots.random_action()
            print(f'\nRound {round_no}: Random suggestion, let\'s {action}')
        elif u_input == "i":    # User wants to choose a suggestion for the clients
            action = input("Suggest an action [verb]: ")
            if not action:
                action = "noth"
            print(f'\nRound {round_no}: The host has suggested {action}ing')
        elif u_input == "k":    # User wants to kick a bot from the chat
            bot_to_kick = input("\nWhich bot should be kicked: ")
            kick(bot_to_kick)   # Attempts to kick the bot with the chosen nickname
        elif u_input == "h":    # User want to see the help menu
            print("")   # Prints empty line for visual clarity
            help()  # Prints list of commands
        elif u_input == "q":    # User wants to close the chat
            print("\nThank you for using Thea\'s bots! You will now be disconnected")
            break   # Exits the command loop
        else:   # User input an invalid command
            print("\nInvalid command!")
            help()  # Displays list of valid commands

        if u_input == "r" or u_input == "i":    # If user wanted to suggest something
            suggest(action)  # Suggests an action to all connected clients
            round_no += 1   # Increases number of suggestions sent
        elif len(clients) < 2:  # In case someone gets kicked and only one client remains
            print("\nNot enough people left! Closing the chat room...")
            # Broadcast only reaches the one client that is still connected
            broadcast("\nYou are alone! The chat will now close!".encode())
            break   # Exits the command loop

# Sets both booleans to False, so we can exit the program properly
Accepting = False
Running = False

thread.join()   # Stops the thread that accepts new client connections

close_all()  # Closes all client connections that are still active
