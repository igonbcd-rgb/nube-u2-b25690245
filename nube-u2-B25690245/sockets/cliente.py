import socket
c = socket.socket()
c.connect(("localhost", 5000))
while True:
    dato = input("Mensaje: ")
    c.send(dato.encode())
    if dato == "salir":
        break
    print(c.recv(1024).decode())