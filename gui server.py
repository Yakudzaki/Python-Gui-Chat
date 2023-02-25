from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread



def accept_incoming_connections():
    """Настраивает обработку входящих клиентов."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s подключился." % client_address)
        client.send(bytes("Привет от Yakudza!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()



def handle_client(client):  # Принимает клиентский сокет в качестве аргумента.
    """Обрабатывает одно клиентское соединение."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Добро пожаловать, %s! Если вы когда-нибудь захотите выйти, нажмите <> для выхода.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s присоединился к чату!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("<>", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("<>", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s покинул чат." % name, "utf8"))
            break



def broadcast(msg, prefix=""):  # префикс для идентификации имени.
    """Отправляет сообщение всем клиентам."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)



if __name__ == "__main__":
    SERVER.listen(5)
    print("Ожидание подключения...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()