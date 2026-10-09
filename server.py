import shutil
import socket
from PIL import ImageGrab
import pyperclip
import subprocess
import os

def screenshot(client_soc):
        im = ImageGrab.grab()
        im.save(r'screen.jpg')
        # open and read the file as binary data
        with open("screen.jpg", "rb") as f:
            file_data = f.read()
        file_data_len = str(len(file_data)).zfill(6)
        file_name = "screen.jpg"
        file_name_len = str(len(file_name)).zfill(2)

        try:
            client_soc.send(file_name_len.encode())
            client_soc.send(file_name.encode())
            client_soc.send(file_data_len.encode())
            client_soc.send(file_data)
            print("the image file successfully send to the client")
        except Exception as e:
            print(f"{str(e)} - problem send / receive data - try again later")
def copy(client_soc):
        # receive text to copy from the client
        text_len = client_soc.recv(2).decode()
        text_len = int(text_len)
        text_copy = client_soc.recv(text_len).decode()
        pyperclip.copy(text_copy)

        pasted = pyperclip.paste()
        if pasted == text_copy:
            response = str(0)
        else:
            response = str(1)

        response_len = str(len(response)).zfill(2)

        client_soc.send(response_len.encode())
        client_soc.send(response.encode())
def paste(client_soc):
        response = pyperclip.paste()
        response_len = str(len(response)).zfill(2)

        client_soc.send(response_len.encode())
        client_soc.send(response.encode())
def open_program(client_soc):
        prog_len = client_soc.recv(1).decode()
        prog_len = int(prog_len)
        prog_name = client_soc.recv(prog_len).decode()
        try:
            subprocess.Popen(prog_name)
            response = str(0)
        except Exception:
            response = str(1)

        response_len = str(len(response)).zfill(2)
        client_soc.send(response_len.encode())
        client_soc.send(response.encode())
def show_folder(client_soc):
        folder_path_len = int(client_soc.recv(2).decode())
        folder_path = client_soc.recv(folder_path_len).decode()
        if not os.path.isdir(folder_path):
            print("folder doesn't exist - try again")
            return 1
        data = str(os.listdir(folder_path))
        data_len = str(len(data)).zfill(2)
        client_soc.send(data_len.encode())
        client_soc.send(data.encode())

def delete(client_soc):
        file_path_len = int(client_soc.recv(2).decode())
        file_path = client_soc.recv(file_path_len).decode()
        try:
            os.remove(file_path)
            response = "0"
        except Exception:
            response = "1"

        response_len = str(len(response)).zfill(2)
        client_soc.send(response_len.encode())
        client_soc.send(response.encode())
def copy_file(client_soc):
        copy_path_len = int(client_soc.recv(2).decode())
        copy_path = client_soc.recv(copy_path_len).decode()
        paste_path_len = int(client_soc.recv(2).decode())
        paste_path = client_soc.recv(paste_path_len).decode()
        try:
            shutil.copy(copy_path, paste_path)
            response = str(0)
        except Exception:
            response = str(1)
        response_len = str(len(data)).zfill(2)
        client_soc.send(response_len.encode())
        client_soc.send(response.encode())

# create the server
server_soc = socket.socket()
server_soc.bind(("0.0.0.0", 1450))
server_soc.listen(3)

while True:
    # server waits to clients
    client_soc, addr = server_soc.accept()
    print(f"{addr[0]} - connected")

    # handles the client
    while True:
        try:
            data = client_soc.recv(12).decode()
            if data == "":
                break
            elif data == "1":
                screenshot(client_soc)
                print("the image file successfully send to the client")

            elif data == "2":
                copy(client_soc)
                print("Success copying text")
            elif data == "3":
                paste(client_soc)
                print("Pasted Successfully")
            elif data == "4":
                open_program(client_soc)
            elif data == "5":
                returnVal = show_folder(client_soc)
                if returnVal == 1:
                    print("Path doesn't exist - try again")
                    continue
                print("Success")
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