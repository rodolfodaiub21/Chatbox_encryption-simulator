import socket
import threading
from Crypto.Cipher import AES, DES
from Crypto.Util import Padding
import base64
from Get_key import DES_KEY1 as k1
from Get_key import DES_KEY2 as k2
from Get_key import DES_KEY3 as k3
from Get_key import AES_KEY as ak
clients = []

def decipher_AES(ciphertext):
    dcipher = AES.new(ak, AES.MODE_ECB)
    try:
        message = Padding.unpad(dcipher.decrypt(ciphertext), 16, style='pkcs7')
        return message
    except Exception as e:
        print("AES padding error:", e)
        return None

def decipher_3DES(ciphertext):
    dcipher1 = DES.new(k3, DES.MODE_ECB)
    dcipher2 = DES.new(k2, DES.MODE_ECB)
    dcipher3 = DES.new(k3, DES.MODE_ECB)
    return Padding.unpad(dcipher1.decrypt(dcipher2.decrypt(dcipher3.decrypt(ciphertext))), 8, style='pkcs7')

def decipher_DES(ciphertext):
    dcipher = DES.new(k1, DES.MODE_ECB)
    return Padding.unpad(dcipher.decrypt(ciphertext), 8, style='pkcs7').decode('utf-8')

def decipher(ciphertext):
    step1 = decipher_AES(ciphertext)
    if step1 is None:
        return "[ERROR] AES decryption failed"
    step2 = decipher_3DES(step1)
    step3 = decipher_DES(step2)
    return step3

def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected.")
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break

            print(f"[{address}] : {message}")
            raw_bytes = base64.b64decode(message.decode('utf-8'))
            deciphered_message = decipher(raw_bytes)
            broadcast(deciphered_message.encode(), client_socket)
        except Exception as e:
            print(f"[ERROR] from {address}: {e}")
            break

    print(f"[DISCONNECT] {address} disconnected.")
    clients.remove(client_socket)
    client_socket.close()

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(message)
            except:
                client.close()
                clients.remove(client)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5555))
    server.listen()
    print("Chatroom is working")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    main()
