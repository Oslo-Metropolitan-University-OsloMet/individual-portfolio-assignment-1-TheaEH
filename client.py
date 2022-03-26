import sys          # to access command line arguments
import socket       # to use sockets in our program
import threading    # to use threads
import bots         # to use the bot commands from another .py file

# Creates a socket using TCP/IP protocol
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Checks to see if we have received the correct amount of cl arguments
if len(sys.argv) != 4:  # Displays the correct values of the cl arguments, can be called with -h
    print("Command line arguments should be: ip-address, port-number, bot-name")
    exit()

IP_address = str(sys.argv[1])       # Takes the first argument from command prompt as IP address

Port = int(sys.argv[2])             # Takes the second argument from command prompt as port number

Bot = str(sys.argv[3]).lower()      # Takes the third argument from command prompt as bot

clientSocket.connect((IP_address, Port))    # Connects to the TCP socket

if Bot == "user":                   # The user can choose the nickname of the user input-based bot
    nickname = input("Choose a nickname: ").capitalize()
else:                               # The nickname of a regular bot is always the bot's own name
    nickname = Bot.capitalize()


def receive():
    while True:
        try:
            msg = clientSocket.recv(1024).decode()
            sentence = msg.split(" ")
            if msg == 'NICK':               # Server requests the client's nickname
                clientSocket.send(nickname.encode())
            elif msg == "CONN":             # Server checks if the connection is still active
                clientSocket.send("y".encode())
            elif sentence[0] == "SUGG":     # Server sends a suggestion for the bot to reply to
                suggested_action = sentence[-1]
                reply = bots.get_reply(Bot, suggested_action)       # Fetches a reply from the bot
                clientSocket.send(f'{nickname}: {reply}'.encode())  # Sends the reply to the server
            else:                           # The received message is not a request for anything
                if msg != "":               # The message is a reply from another bot
                    print(msg)
                else:                       # The message is empty, which means the connection has been closed
                    print("\nDisconnecting from the server...")
                    break
        except socket.error as e:           # This exception occurs if the socket is closed by the host
            print("\n(You have been disconnected from the server!)")
            break


receive_thread = threading.Thread(target=receive)  # Creates a thread for the bot to receive messages
receive_thread.start()      # The bot receives messages for as long as it is connected
