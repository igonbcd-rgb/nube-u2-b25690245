from cryptography.fernet import Fernet # AES-128-CBC + HMAC-SHA256

llave = Fernet.generate_key() # guardar en KMS / Secrets Manager
f = Fernet(llave)
with open("clientes.csv", "rb") as a:
    cifrado = f.encrypt(a.read())
with open("clientes.csv.enc", "wb") as a:
    a.write(cifrado)

original = f.decrypt(cifrado) # falla si el archivo fue alterado