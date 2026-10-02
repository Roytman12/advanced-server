import shutil
import socket
import random
from datetime import datetime
from PIL import ImageGrab
import pyperclip
import subprocess
import os

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
            data = client_soc.recv(1024).decode()
            if data == "":
                break
            if data == "screenshot":
                im = ImageGrab.grab()
                im.save(r'screen.jpg')
                # open and read the file as binary data
                with open("screen.jpg", "rb") as f:
                    file_data = f.read()
                file_data_len = str(len(file_data)).zfill(6)
                file_name = "screen.jpg"
                file_name_len = str(len(file_name)).zfill(6)

                try:
                    client_soc.send(file_name_len.encode())
                    client_soc.send(file_name.encode())
                    client_soc.send(file_data_len.encode())
                    client_soc.send(file_data)
                    print("the image file successfully send to the client")
                except Exception as e:
                    print(f"{str(e)} - problem send / receive data - try again later")
                    break

            elif data == "copy":
                try:
                    # receive text to copy from the client
                    text_copy = client_soc.recv(1024).decode()
                    copy = pyperclip.copy(text_copy)
                    print("Success copying text")

                    response = "Copy successful"
                    response_len = str(len(response)).zfill(2)

                    client_soc.send(response_len.encode())
                    client_soc.send(response.encode())

                    print(pyperclip.paste())
                except Exception as e:
                    print(f"error in recv/send {str(e)}")
            elif data == "paste":
                try:
                    response = pyperclip.paste()
                    response_len = str(len(response)).zfill(2)

                    client_soc.send(response_len.encode())
                    client_soc.send(response.encode())
                except Exception as e:
                    print(f"error in recv/send {str(e)}")

            elif data == "open_program":
                try:
                    prog_name = client_soc.recv(50).decode()
                    try:
                        subprocess.Popen(prog_name)
                        response = "Program launched successfully"
                    except Exception:
                        response = "Program failed to launch"

                    response_len = str(len(response)).zfill(2)
                    client_soc.send(response_len.encode())
                    client_soc.send(response.encode())
                except Exception as e:
                    print(f"error in recv/send {str(e)}")
            elif data == "show_folder":
                try:
                    folder_path = client_soc.recv(50).decode()
                    data = str(os.listdir(folder_path))
                    data_len = str(len(data)).zfill(2)
                    client_soc.send(data_len.encode())
                    client_soc.send(data.encode())
                except Exception as e:
                    print(f"error in recv/send {str(e)}")
            elif data == "delete":
                try:
                    file_path = client_soc.recv(50).decode()
                    try:
                        os.remove(file_path)
                        response = "Success"
                    except Exception:
                        response = "Failed to delete the file"
                    response_len = str(len(data)).zfill(2)
                    client_soc.send(response_len.encode())
                    client_soc.send(response.encode())
                except Exception as e:
                    print(f"error in recv/send {str(e)}")

            elif data == "copy_file":
                try:
                    copy_path = client_soc.recv(50).decode()
                    paste_path = client_soc.recv(50).decode()
                    try:
                        shutil.copy(copy_path, paste_path)
                        response = "Success"
                    except Exception:
                        response = "Failed to copy the file"
                    response_len = str(len(data)).zfill(2)
                    client_soc.send(response_len.encode())
                    client_soc.send(response.encode())
                except Exception as e:
                    print(f"error in recv/send {str(e)}")
            else:
                print(f"getting data - {data}")
                client_soc.send(data.encode())
        except Exception as e:
            print(f"error in recv/send {str(e)}")
            break
    print(f"{addr[0]} - disconnected")
    client_soc.close()