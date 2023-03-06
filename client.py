import socket
import threading

HOST = "localhost"
PORT = 12345


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


logo = f"""
{Clrs.BLU} @@@@@@  @@@@@@  @  @@@@@@@  @@@@@@  @@@@@@@ {Clrs.BLD}
{Clrs.CYN}!@@     @@!  @@@   !@@      @@!  @@@   @!!    
{Clrs.BLD} !@@!!  @!@  !@!   !@!      @!@!@!@!   @!!    
{Clrs.BLD}    !:! !!:  !!!   :!!      !!:  !!!   !!:    
{Clrs.RED}::.: :   : :. :     :: :: :  :   : :    :    {Clrs.PIK}(=^-ω-^=){Clrs.END}
"""


def receive_message():
    while True:
        data = s.recv(1024).decode()
        if not data:
            break
        print(data)


def send_message(nickname):
    while True:
        try:
            message = input()
            if message == "q":
                print(f"{Clrs.RED}Good bye {nickname} (=ච ﻌ ච=){Clrs.END}")
                break
            elif len(message):
                s.send(f"{Clrs.CYN}{nickname}:{Clrs.END} {message}".encode())
        except BrokenPipeError:
            print(f"{Clrs.RED}Enough talking! (=🝦 ﻌ 🝦=) The server is tired.{Clrs.END}")
            break


def client():
    try:
        nickname = None
        data = s.recv(1024).decode()
        if nickname is None:
            print(f"{Clrs.YEL}{data}{Clrs.END}")
            print(f"{logo}")
            nickname = input(f"{Clrs.YEL}Tell me your nickname, please: {Clrs.END}")
            s.send(nickname.encode())
            print(
                f"{Clrs.GRN}Well, {nickname}, let's chat! {Clrs.UDL}Use q for exit!{Clrs.END}"
            )

        send_thread = threading.Thread(
            target=send_message, args=(nickname,), daemon=True
        )
        send_thread.start()
        receive_thread = threading.Thread(target=receive_message, daemon=True)
        receive_thread.start()

        send_thread.join()
    except KeyboardInterrupt:
        print(f"\n{Clrs.RED}Bye (=ච ﻌ ච=){Clrs.END}")
        exit(0)


if __name__ == "__main__":
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            client()
    except ConnectionRefusedError:
        print(f"{Clrs.RED}Enough talking! (=🝦 ﻌ 🝦=) The server is tired.{Clrs.END}")
        exit(0)
