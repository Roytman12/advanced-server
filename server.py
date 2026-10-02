import socket
import threading
import os
import shutil

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


server_soc = socket.socket()
server_soc.bind(("0.0.0.0", 1450))
server_soc.listen(3)


while True:
    client_socket, addr = server_soc.accept()
    print(f"{addr[0]} - connected")

    while True:
        try:
            # trying to receive the image
            file_name_len = int(client_socket.recv(2).decode())
            file_name = client_socket.recv(file_name_len).decode()
            file_data_len = int(client_socket.recv(6).decode())
            recv_image_data(client_socket, file_name, file_data_len)
            print("Image Transferred successfully")

            # putting the image inside a folder
            folder = "image_folder"
            os.makedirs(folder, exist_ok= True)
            shutil.move(file_name, os.path.join(folder, file_name))
            # open the image
            os.startfile(os.path.join(folder, file_name))
        except Exception as e:
            print(f"client {addr[0]} disconnected due to {str(e)}")
            client_socket.close()
            break

