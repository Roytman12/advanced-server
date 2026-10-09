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

def screenshot(my_sock, msg):
    my_sock.send(msg.encode())
    # trying to receive the image
    file_name_len = int(my_sock.recv(2).decode())
    file_name = my_sock.recv(file_name_len).decode()
    file_data_len = int(my_sock.recv(6).decode())
    recv_image_data(my_sock, file_name, file_data_len)
    print("Image Transferred successfully")

    # open the image
    im = Image.open('screen.jpg')
    im.show()

def copy(my_sock, msg):
    my_sock.send(msg.encode())
    text = input("Enter Text to Copy:")
    str_len = str(len(text)).zfill(2)
    my_sock.send(str_len.encode())
    my_sock.send(text.encode())
    reqLen = my_sock.recv(2).decode()
    data = my_sock.recv(int(reqLen)).decode()
    print(f"server sent - {data}")

def paste(my_sock, msg):
    my_sock.send(msg.encode())
    reqLen = my_sock.recv(2).decode()
    data = my_sock.recv(int(reqLen)).decode()
    print(f"server sent - {data}")

def open_program(my_sock, msg):
    my_sock.send(msg.encode())
    prog = input("enter a program the sever needs to open:")
    prog_len = str(len(prog)).zfill(1)
    my_sock.send(prog_len.encode())
    my_sock.send(prog.encode())
    reqLen = my_sock.recv(2).decode()
    data = my_sock.recv(int(reqLen)).decode()
    print(f"server sent - {data}")

def show_folder(my_sock, msg):
    my_sock.send(msg.encode())
    folder_path = input("Enter folder path:")
    folder_path_len = str(len(folder_path)).zfill(2)
    my_sock.send(folder_path_len.encode())
    my_sock.send(folder_path.encode())

    reqLen = my_sock.recv(2).decode()
    data = my_sock.recv(int(reqLen)).decode()
    print(f"server sent - {data}")

def delete(my_sock, msg):
    my_sock.send(msg.encode())
    file_path = input("Enter file path:")
    file_path_len = str(len(file_path)).zfill(2)
    my_sock.send(file_path_len.encode())
    my_sock.send(file_path.encode())

    reqLen = my_sock.recv(2).decode()
    data = my_sock.recv(int(reqLen)).decode()
    print(f"server sent - {data}")

def copy_file(my_sock, msg):
    my_sock.send(msg.encode())
    copy_path = input("Enter file path to copy:")
    copy_path_len = str(len(copy_path)).zfill(2)
    my_sock.send(copy_path_len.encode())
    my_sock.send(copy_path.encode())

    paste_path = input("Enter file path to paste:")
    paste_path_len = str(len(copy_path)).zfill(2)
    my_sock.send(paste_path_len.encode())
    my_sock.send(paste_path.encode())

    reqLen = my_sock.recv(2).decode()
    data = my_sock.recv(int(reqLen)).decode()
    print(f"server sent - {data}")


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
    msg = input("""Enter one of the following commands:
1 = Screenshot
2 = Copy
3 = Paste
4 = Open a Program
5 = show folder's files
6 =  delete
7 = copy file
8 = exit""")
    if msg.lower() == "8":
        break
    try:
        if msg == "1":
                screenshot(my_sock, msg)
        elif msg == "2":
                copy(my_sock, msg)
        elif msg == "3":
                paste(my_sock, msg)
        elif msg == "4":
                open_program(my_sock, msg)
        elif msg == "5":
                show_folder(my_sock, msg)
        elif msg == "6":
                delete(my_sock, msg)
        elif msg == "7":
                copy_file(my_sock, msg)
        else:
            break
    except Exception as e:
        print(f"error: {str(e)}")
my_sock.close()
print("Bye Bye")