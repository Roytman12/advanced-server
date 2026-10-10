import shutil
import socket
from PIL import ImageGrab
import pyperclip
import subprocess
import os

def send_data(client_soc, data_len, data):
    """
    sends data to the client
    :param client_soc: socket
    :param data_len: int
    :param data: str
    :return: no return
    """
    client_soc.send(str(len(data)).zfill(data_len).encode())
    client_soc.send(data)

def screenshot(client_soc):
        """
        takes a screenshot and sending it to the client
        :param client_soc: socket
        :return: sends screenshot to the client
        """
        im = ImageGrab.grab()
        im.save(r'screen.jpg')
        # open and read the file as binary data
        with open("screen.jpg", "rb") as f:
            file_data = f.read()
        file_name = "screen.jpg"

        try:
            send_data(client_soc,2, file_name.encode())
            send_data(client_soc, 6, file_data)
            print("the image file successfully send to the client")
        except Exception as e:
            print(f"{str(e)} - problem send / receive data - try again later")
def copy(client_soc):
        """
        receives a text from the client and copies it to the clipboard
        :param client_soc: socket
        :return: 0 if succeeded or 1 if failed
        """
        # receive text to copy from the client
        text_len = client_soc.recv(2).decode()
        text_len = int(text_len)
        text_copy = client_soc.recv(text_len).decode()
        pyperclip.copy(text_copy)

        pasted = pyperclip.paste()
        if pasted == text_copy:
            response = "0"
        else:
            response = "1"

        send_data(client_soc, 2, response.encode())
def paste(client_soc):
        """
        Pastes the text from the clipboard and sending it the client
        :param client_soc: socket
        :return: 0 if succeeded or 1 if failed
        """
        response = pyperclip.paste()
        send_data(client_soc,2, response.encode())
def open_program(client_soc):
        """
        receives a program from the client and opens it
        :param client_soc: socket
        :return: 0 if succeeded or 1 if failed
        """
        prog_len = client_soc.recv(1).decode()
        prog_len = int(prog_len)
        prog_name = client_soc.recv(prog_len).decode()
        try:
            subprocess.Popen(prog_name)
            response = "0"
        except Exception:
            response = "1"

        send_data(client_soc, 2, response.encode())
def show_folder(client_soc):
        """
        receives a path from the client and sending the folder data to the client
        :param client_soc: socket
        :return: 0 if succeeded or 1 if failed
        """
        folder_path_len = int(client_soc.recv(2).decode())
        folder_path = client_soc.recv(folder_path_len).decode()
        if not os.path.isdir(folder_path):
            print("folder doesn't exist - try again")
            return 1
        data = str(os.listdir(folder_path))
        send_data(client_soc, 2, data.encode())
def delete(client_soc):
        """
        gets a path from the client and deletes the file in that path
        :param client_soc: socket
        :return: 0 if succeeded, 1 if failed
        """
        file_path_len = int(client_soc.recv(2).decode())
        file_path = client_soc.recv(file_path_len).decode()
        try:
            os.remove(file_path)
            response = "0"
        except Exception:
            response = "1"

        send_data(client_soc,2,response.encode())
def copy_file(client_soc):
        """
        gets a path from the client and copies it into a new path
        :param client_soc: socket
        :return: 0 if succeeded, 1 if failed
        """
        copy_path_len = int(client_soc.recv(2).decode())
        copy_path = client_soc.recv(copy_path_len).decode()
        paste_path_len = int(client_soc.recv(2).decode())
        paste_path = client_soc.recv(paste_path_len).decode()
        try:
            shutil.copy(copy_path, paste_path)
            response = "0"
        except Exception:
            response = "1"
        send_data(client_soc,2, response.encode())

# create the server
server_soc = socket.socket()
server_soc.bind(("0.0.0.0", 1450))
server_soc.listen(3)
while True:
    # server waits to clients
    client_soc, addr = server_soc.accept()
    print(f"{addr[0]} - connected")
    while True:
        try:
            data = client_soc.recv(2).decode()
            if data == "":
                break
            elif data == "1":
                screenshot(client_soc)
            elif data == "2":
                copy(client_soc)
            elif data == "3":
                paste(client_soc)
            elif data == "4":
                open_program(client_soc)
            elif data == "5":
                returnVal = show_folder(client_soc)
                if returnVal == 1:
                    continue
            elif data == "6":
                delete(client_soc)
            elif data == "7":
                copy_file(client_soc)
            else:
                break
        except Exception as e:
            print(f"error in recv/send {str(e)}")
            break
    print(f"{addr[0]} - disconnected")
    client_soc.close()