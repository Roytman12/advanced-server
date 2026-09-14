import socket

my_sock = socket.socket()
# Connect to server
try:
    my_sock.connect(("127.0.0.1", 1450))
# if it didn't work, close the socket and end the program.
except Exception as e:
    my_sock.close()
    exit(f"Connection Failed - try again {str(e)}")


while True:
    msg = input("Enter msg to send or q to finish")
    if msg.lower() == "q":
        break

    try:
        my_sock.send(msg.encode())
        data = my_sock.recv(1024).decode()
        print(f"server sent - {data}")
    except Exception as e:
        print(f"error in receive or sending data {str(e)}")
        break

my_sock.close()
print("Bye Bye")