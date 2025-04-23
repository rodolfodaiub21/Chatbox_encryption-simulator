import socket
import threading
from Crypto.Cipher import AES, DES
from Crypto.Util import Padding
import base64
from Get_key import DES_KEY1 as k1
from Get_key import DES_KEY2 as k2
from Get_key import DES_KEY3 as k3
from Get_key import AES_KEY as ak
import sys
def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024)
            if not message:
                break
            stop_input = True
            sys.stdout.write('\r' + ' ' * 100 + '\r')
            print("\n" + message.decode())
            sys.stdout.write(f"{user}: ")
            sys.stdout.flush()
        except:
            print("[ERROR] Connection closed.")
            sock.close()
            break

def encryption_DES(plaintext):
    cipher = DES.new(k1, DES.MODE_ECB)
    pad = Padding.pad(plaintext.encode('utf-8'), 8, style='pkcs7')
    return cipher.encrypt(pad)

def encryption_3DES(plaintext):
    cipher1 = DES.new(k3, DES.MODE_ECB)
    cipher2 = DES.new(k2, DES.MODE_ECB)
    cipher3 = DES.new(k3, DES.MODE_ECB)
    pad = Padding.pad(plaintext, 8, style='pkcs7')
    return cipher3.encrypt(cipher2.encrypt(cipher1.encrypt(pad)))

def encryption_AES(plaintext):
    cipher = AES.new(ak, AES.MODE_ECB)
    pad = Padding.pad(plaintext, 16, style='pkcs7')
    return cipher.encrypt(pad)

def cipher_message(message):
    step1 = encryption_DES(message)
    #print("DES encryption: ",step1)
    step2 = encryption_3DES(step1)
    #print("3DES encryption2 ",step2)
    step3 = encryption_AES(step2)
    #print("AES encryption",step3)
    #.rint("Final deliver",base64.b64encode(step3).decode('utf-8'))
    return base64.b64encode(step3).decode('utf-8')

def main():
    global user
    user = input("Give me your username: ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5555))

    print(f"Welcome {user} to the ChatBox server, You can start to talk now")

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon=True
    thread.start()

    while True:
        message = input(f"{user}: ")
        if message.lower() == 'exit':
            break
        full_message = f"{user}: {message}"
        encrypted = cipher_message(full_message)
        client.sendall(encrypted.encode())

    client.close()

if __name__ == "__main__":
    #print(ak)
    main()
