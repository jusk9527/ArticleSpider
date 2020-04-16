import anyio
import typing
import ssl


class SocketStream:
    async def receive_some(self) -> bytes:
        pass

    async def send_all(self, data: bytes) -> None:
        pass

    async def close(self) -> None:
        pass

    async def start_tls(self, ssl_context: ssl.SSLContext, server_hostname: typing.Optional[str]) -> "SocketStream":
        pass


class Backend:
    async def connect_tcp(self, address, port, *, server_hostname: typing.Optional[str], ssl_context: typing.Optional[ssl.SSLContext]=None, autostart_tls: bool=True) -> anyio.SocketStream:
        return await anyio.connect_tcp(address, port, ssl_context=ssl_context, autostart_tls=autostart_tls, tls_standard_compatible=False)

    async def sleep(self, amount: float) -> None:
        await anyio.sleep(amount)

    def create_lock(self) -> anyio.Lock:
        return anyio.Lock()

    def create_queue(self, max_size: int) -> anyio.Queue:
        return anyio.create_queue(max_size)

    def create_event(self) -> anyio.Event:
        return anyio.create_event()

    def create_semaphore(self, max_size: int) -> anyio.Semaphore:
        return anyio.create_semaphore(max_size)
