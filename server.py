import socket

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
            print(f"getting data - {data}")
            client_soc.send(data.encode())
        except Exception as e:
            print(f"error in recv/send {str(e)}")
            break
    print(f"{addr[0]} - disconnected")
    client_soc.close()