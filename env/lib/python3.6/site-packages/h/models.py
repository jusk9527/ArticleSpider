import attr
import typing


@attr.s
class URL:
    scheme: str = attr.ib()
    username: str
    password: str
    host: str
    path: str
    query: str
    fragment: str

    @property
    def target(self) -> str:
        return (
            f"{(self.path or '/')}"
            f"{'?' + self.query if self.query is not None else ''}"
        )


class Request:
    method: str
    url: URL
    headers: dict
    stream_id: int

    data: typing.Optional[typing.Union["SyncRequestData", "AsyncRequestData"]]


class SyncRequestData:
    def content_type(self) -> str:
        pass

    def content_length(self) -> typing.Optional[int]:
        pass

    def read(self, amount: int) -> bytes:
        pass

    def rewind(self) -> None:
        pass

    def is_rewindable(self) -> bool:
        pass


class AsyncRequestData(SyncRequestData):
    async def read(self, amount: int) -> bytes:
        pass

    async def rewind(self) -> bytes:
        pass


class SyncResponse:
    request: Request
    status_code: int
    headers: dict

    _connection: typing.Any = None

    def wait(self) -> None:
        pass

    def raise_on_status(self) -> None:
        pass

    def stream(self) -> typing.Iterable[bytes]:
        pass

    def stream_text(self) -> typing.Iterable[str]:
        pass

    def data(self) -> bytes:
        pass

    def text(self) -> str:
        pass

    def json(self) -> dict:
        pass

    def close(self) -> None:
        pass


class AsyncResponse:
    request: Request
    status_code: int
    headers: dict

    _connection: typing.Any = None

    async def wait(self) -> None:
        pass

    async def raise_on_status(self) -> None:
        pass

    async def stream(self) -> typing.AsyncIterable[bytes]:
        pass

    async def stream_text(self) -> typing.AsyncIterable[str]:
        pass

    async def data(self) -> bytes:
        pass

    async def text(self) -> str:
        pass

    async def json(self) -> dict:
        pass

    async def close(self) -> None:
        pass
