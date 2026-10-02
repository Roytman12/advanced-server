import socket
from PIL import Image
import pyperclip

def recv_image_data(client_socket, file_name, file_data_len):
    """
    receive the image data and save the image
    :param client_socket: the client socket
    :param file_name:  the image file name
    :param file_data_len: the length of the image data
    :return:None
    """

    data = b''
    while len(data) < file_data_len:
        slice = file_data_len - len(data)
        if slice > 1024:
            data += client_socket.recv(1024)
        else:
            data += client_socket.recv(slice)
            break

    # create the image file
    with open (file_name, "wb") as f:
        f.write(data)

# Git repo: https://github.com/Roytman12/advanced-server

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
    if msg.lower() == "screenshot":
            try:
                my_sock.send(msg.encode())
                # trying to receive the image
                file_name_len = int(my_sock.recv(6).decode())
                file_name = my_sock.recv(file_name_len).decode()
                file_data_len = int(my_sock.recv(6).decode())
                recv_image_data(my_sock, file_name, file_data_len)
                print("Image Transferred successfully")

                # open the image
                im = Image.open('screen.jpg')
                im.show()
            except Exception as e:
                print(f"error due to {str(e)}")
                break
    elif msg.lower() == "copy":
        try:
            my_sock.send(msg.encode())
            text = input("Enter Text to Copy:")
            my_sock.send(text.encode())
            reqLen = my_sock.recv(2).decode()
            data = my_sock.recv(int(reqLen)).decode()
            print(f"server sent - {data}")
        except Exception as e:
            print(f"error in receive or sending data {str(e)}")
            break
    elif msg.lower() == "paste":
        try:
            my_sock.send(msg.encode())
            reqLen = my_sock.recv(2).decode()
            data = my_sock.recv(int(reqLen)).decode()
            print(f"server sent - {data}")
        except Exception as e:
            print(f"error in receive or sending data {str(e)}")
            break
    elif msg.lower() == "open_program":
        try:
            my_sock.send(msg.encode())
            prog = input("enter a program the sever needs to open:")
            my_sock.send(prog.encode())
            reqLen = my_sock.recv(2).decode()
            data = my_sock.recv(int(reqLen)).decode()
            print(f"server sent - {data}")
        except Exception as e:
            print(f"error in receive or sending data {str(e)}")
            break
    elif msg.lower() == "show_folder":
        try:
            my_sock.send(msg.encode())
            folder_path = input("Enter folder path:")
            my_sock.send(folder_path.encode())

            reqLen = my_sock.recv(2).decode()
            data = my_sock.recv(int(reqLen)).decode()
            print(f"server sent - {data}")
        except Exception as e:
            print(f"error in receive or sending data {str(e)}")
            break
    elif msg.lower() == "delete":
        try:
            my_sock.send(msg.encode())
            file_path = input("Enter file path:")
            my_sock.send(folder_path.encode())

            reqLen = my_sock.recv(2).decode()
            data = my_sock.recv(int(reqLen)).decode()
            print(f"server sent - {data}")
        except Exception as e:
            print(f"error in receive or sending data {str(e)}")
            break
    elif msg.lower() == "copy_file":
        try:
            my_sock.send(msg.encode())
            copy_path = input("Enter file path to copy:")
            my_sock.send(copy_path.encode())
            paste_path = input("Enter file path to paste:")
            my_sock.send(paste_path.encode())

            reqLen = my_sock.recv(2).decode()
            data = my_sock.recv(int(reqLen)).decode()
            print(f"server sent - {data}")
        except Exception as e:
            print(f"error in receive or sending data {str(e)}")
            break
my_sock.close()
print("Bye Bye")