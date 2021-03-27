import socket
import sys
import typing as t

from utils.config import HEADER_LENGTH
from utils.logger import get_logging
from utils.utils import get_color


def get_header(message: bytes) -> bytes:
    return f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")


def receive_message(sock: socket.socket) -> tuple:
    header = sock.recv(HEADER_LENGTH)

    if not len(header):
        print(get_logging("error", True) + f"{get_color('RED')} Server has closed the connection.")
        sys.exit(1)

    username_len = int(header.decode('utf-8').strip())
    username = sock.recv(username_len).decode('utf-8')

    msg_length = int(sock.recv(HEADER_LENGTH).decode('utf-8').strip())
    msg = sock.recv(msg_length).decode('utf-8')

    return username, msg


def send_message(message: t.Optional[str], sock: socket.socket) -> None:
    if message:
        message = message.replace("\n", "").encode("utf-8")
        message_header = get_header(message)

        sock.send(message_header + message)
