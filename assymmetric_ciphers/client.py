import random
import socket
import time
from encryption import Encryption

class Keys:
    # ключи шифрования
    def __init__(self):
        self.a = random.randint(100, 100000)
        self.g = random.randint(50000, 100000)
        self.p = random.randint(100, 49999)
        self.A = self.g ** self.a % self.p
        self.B = 0
        self.status = True

    def get_K(self):
        K = self.B ** self.a % self.p
        return K

key = Keys()
enc = Encryption()  # шифр

# ip и порт
sock = socket.socket()
server = input('Enter Server: ')  # 'localhost'
port = input('Enter Port: ')  # 9090
print()

# подключение к серверу
try:
    sock.connect((server, int(port)))
    # сервер
    print(f"Server IP: {server}; Port: {port}")

    # клиент
    host = sock.getsockname()
    print(f"Client IP: {host[0]}; Port: {host[1]}")
except ConnectionRefusedError as c:
    print(f"ERROR: {c}")


# main
while True:
    if key.status:
        # отправляем ключи серверу
        sock.send(f'key-A: {key.A}'.encode())
        time.sleep(0.3)
        sock.send(f'key-g: {key.g}'.encode())
        time.sleep(0.3)
        sock.send(f'key-p: {key.p}'.encode())
        time.sleep(0.3) # тайм слип для избежания ошибки (сервер может не успеть обработаь сообщение)
        print(f'key-A: {key.A}\nkey-g: {key.g}\nkey-p: {key.p}')

        # шифрование
        while True:
            data = sock.recv(1024).decode("utf8")
            if data[:5] == 'key-B':
                key.B = int(data.split(' ')[1])
                print(key.a)
                print(f'key-B: {key.B}')
                print(f'key-K: {key.get_K()}')
            if key.B != 0:
                break
        key.status = False

    # сообщения от клиента
    msg = input("\nYou: ")
    new_msg = enc.Msg_Bytes(msg, key.get_K())
    sock.send(new_msg.encode())

    # отключение от сервера
    if len(msg) == 0 or msg.lower() == 'stop' or msg.lower() == 'exit':
        print("You disconnected.")
        break

    # сообщения от сервера
    try:
        old_data = sock.recv(1024).decode("utf8")
        data = enc.Bytes_Msg(old_data, key.get_K())
        print(f"\nServer: {data}")
    except ConnectionResetError as e:
        print(f"ERROR: {e}")
        break

sock.close()
