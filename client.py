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

def send_data(client_soc, data_len, data):
    """
    sends data to the client
    :param client_soc: socket
    :param data_len: int
    :param data: str
    :return: no return
    """
    try:
        client_soc.send(str(len(data)).zfill(data_len).encode())
        client_soc.send(data)
    except Exception as e:
        print(f"error in sending data {str(e)}")

def recv_data(client_soc, data_len):
    """
    receives data to the client
    :param client_soc: socket
    :param data_len: int
    :param data: str
    :return: no return
    """
    try:
        data_len = my_sock.recv(2).decode()
        data = my_sock.recv(int(data_len)).decode()
    except Exception as e:
        print(f"error in sending data {str(e)}")
    print(f"server sent - {data}")
    return data, data_len

def screenshot(my_sock, msg):
    """
    receives a screenshot from the server
    :param my_sock: socket
    :param msg: str
    :return: none
    """
    my_sock.send(msg.encode())
    # trying to receive the image

    file_name, file_name_len = recv_data(my_sock, 2)
    file_data_len = int(my_sock.recv(6).decode())
    recv_image_data(my_sock, file_name, file_data_len)
    print("Image Transferred successfully")

    # open the image
    im = Image.open('screen.jpg')
    im.show()

def copy(my_sock, msg):
    """
     sends to the server str to copy to the server clipboard
    :param my_sock: socket
    :param msg: str
    :return: none
    """
    my_sock.send(msg.encode())
    text = input("Enter Text to Copy:")
    send_data(my_sock, 2, text.encode())
    recv_data(my_sock, 2)

def paste(my_sock, msg):
    """
    gets the clipboard from the server
    :param my_sock: socket
    :param msg: str
    :return: none
    """
    my_sock.send(msg.encode())
    recv_data(my_sock, 2)

def open_program(my_sock, msg):
    """
    sends a program name to the server
    :param my_sock: socket
    :param msg: str
    :return: none
    """
    my_sock.send(msg.encode())
    prog = input("enter a program the sever needs to open:")
    send_data(my_sock, 1, prog.encode())
    recv_data(my_sock,2)

def show_folder(my_sock, msg):
    """
    sends a path to the server and receives the folder's data
    :param my_sock: socket
    :param msg: str
    :return: none
    """
    my_sock.send(msg.encode())
    folder_path = input("Enter folder path:")
    send_data(my_sock,2, folder_path.encode())

    recv_data(my_sock, 2)

def delete(my_sock, msg):
    """
    sends a path to the server and receives 1 or 0 if the file was deleted
    :param my_sock: socket
    :param msg: str
    :return: none
    """
    my_sock.send(msg.encode())
    file_path = input("Enter file path:")
    file_path_len = str(len(file_path)).zfill(2)
    send_data(my_sock,2,file_path.encode())
    recv_data(my_sock, 2)

def copy_file(my_sock, msg):
    """
    sends a path to the server and receives 1 or 0 if it duplicated it or not
    :param my_sock: socket
    :param msg: str
    :return: none
    """
    my_sock.send(msg.encode())
    copy_path = input("Enter file path to copy:")
    send_data(my_sock, 2, copy_path.encode())
    paste_path = input("Enter file path to paste:")
    send_data(my_sock, 2, paste_path.encode())

    recv_data(my_sock, 2)
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

my_sock.close()
print("Bye Bye")