import socket
import threading
import logging


class Clrs:
    PIK = "\033[35m"
    BLU = "\033[34m"
    CYN = "\033[36m"
    GRN = "\033[32m"
    YEL = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"
    BLD = "\033[1m"
    UDL = "\033[4m"


HOST = "127.0.0.1"
PORT = 12345

clients = {}
nicknames = set()
user_log = {}


def send_all(client_id, data):
    for c_id, c_conn in clients.items():
        if c_id != client_id:
            c_conn.sendall(f"{hint} {data}".encode())


def client_disconnected(client_id, nickname):
    if nicknames and nickname in nicknames:
        nicknames.remove(nickname)
        send_all(client_id, f"{Clrs.RED}{nickname} left the chat{Clrs.END}")
    logging.info(f"{Clrs.RED}Client {client_id} disconnected.{Clrs.END}")
    del clients[client_id]


def first_connect(connect, nickname):
    if len(nicknames):
        data = f"{Clrs.PIK}Chat now: {', '.join(nicknames)}{Clrs.END}"
    else:
        data = f"{Clrs.PIK}Nobody here yet.{Clrs.END}"
    nicknames.add(nickname)
    connect.send(data.encode())


def handle_client(connection, address) -> socket:
    client_id = len(clients) + 1
    clients[client_id] = connection
    nickname = None
    connection.send("Hello stranger! Welcome to ".encode())

    while True:
        try:
            data = connection.recv(1024).decode()
            if not len(data):
                client_disconnected(client_id, nickname)
                break
            elif nickname is None:
                nickname = data
                first_connect(connection, nickname)
                send_all(
                    client_id, f"{Clrs.BLU}{nickname} has joined the chat!{Clrs.END}"
                )
                continue

            logging.info(
                f"{Clrs.YEL}For FSB {address} {nickname}{data.replace(nickname, '', 1)}{Clrs.END}"
            )
            send_all(client_id, data)

        except ConnectionResetError:
            client_disconnected(client_id, nickname)
            break


if __name__ == "__main__":
    try:
        hint = f"{Clrs.YEL}[ q for exit ]{Clrs.END}"
        frmt = "%(asctime)s: %(message)s"
        logging.basicConfig(format=frmt, level=logging.INFO, datefmt="%H:%M:%S")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_s:
            server_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_s.bind((HOST, PORT))
            server_s.listen()
            sockets_list = [server_s]
            logging.info(f"{Clrs.GRN}Start server{Clrs.END}")

            while True:
                conn, addr = server_s.accept()
                logging.info(f"{Clrs.BLU}New client connected: {addr}{Clrs.END}")
                client_thread = threading.Thread(
                    target=handle_client, args=(conn, addr), daemon=True
                )
                client_thread.start()
    except KeyboardInterrupt:
        logging.info(f"{Clrs.GRN}Stop server{Clrs.END}")
        exit(0)
