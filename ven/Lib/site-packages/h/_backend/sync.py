import socket
import ssl
import typing
import time
import threading
import queue


class SocketStream:
    def __init__(self, sock: socket.socket):
        self.sock = sock

    def receive_some(self) -> bytes:
        pass

    def send_all(self, data: bytes) -> None:
        pass

    def close(self) -> None:
        pass

    def start_tls(self, ssl_context: ssl.SSLContext, server_hostname: typing.Optional[str]) -> "SocketStream":
        pass


class Backend:
    def connect_tcp(self, address: str, *, port: int, server_hostname: typing.Optional[str], ssl_context: typing.Optional[ssl.SSLContext]=None, autostart_tls: bool=True) -> socket.socket:
        sock = socket.create_connection((address, port))
        if hasattr(socket, "TCP_NODELAY"):
            sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
        if ssl_context is not None and autostart_tls:
            sock = ssl_context.wrap_socket(sock, server_hostname=address)
        sock.setblocking(False)
        return sock

    def sleep(self, amount: float) -> None:
        time.sleep(amount)

    def create_lock(self) -> threading.Lock:
        return threading.Lock()

    def create_queue(self, max_size: int) -> queue.Queue:
        return queue.Queue(max_size)

    def create_event(self) -> threading.Event:
        return threading.Event()

    def create_semaphore(self, max_size: int) -> threading.BoundedSemaphore:
        return threading.BoundedSemaphore(max_size)
