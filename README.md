
# 🔐 Encrypted Client-Server Chat Simulator

This project implements a secure real-time chat application using Python's `socket` and `threading` modules, with layered encryption (DES → 3DES → AES) applied to all messages sent between the client and server.

## 📌 Features

- Real-time chat between multiple clients
- Multi-layered encryption using DES, 3DES, and AES
- Base64 encoding for ciphertext transmission
- Threaded server handling concurrent clients

## 🧱 Encryption Cascade

Messages are encrypted as follows:
1. **DES**: ECB + PKCS7 padding
2. **3DES**: DES with two unique keys
3. **AES**: ECB + PKCS7 padding
4. Encoded in **Base64**

Decryption follows the inverse order on the server.

## 🗃️ File Structure

| File         | Description                         |
|--------------|-------------------------------------|
| `Client.py`  | Sends encrypted messages to server  |
| `Server.py`  | Receives, decrypts, and broadcasts  |
| `Get_key.py` | Contains the encryption keys        |
| `requirements.txt` | Lists the Python dependencies |

## 🚀 Getting Started

1. Install dependencies:

2. Run server:
    ```bash
    python Server.py
    ```

3. Run client (in a new terminal):
    ```bash
    python Client.py
    ```

## 🔑 Key File Format (`Get_key.py`)

```python
DES_KEY1 = b'12345678'
DES_KEY2 = b'abcdefgh'
DES_KEY3 = b'87654321'
AES_KEY  = b'mysecretaeskey12'
