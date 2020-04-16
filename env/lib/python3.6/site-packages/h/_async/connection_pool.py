from .connection import Connection
from h.ttp.models import Request, AsyncResponse
from .._backend import AsyncBackend


class ConnectionPool:
    def __init__(self, max_size: int):
        self.backend = AsyncBackend()
        self.pool = self.backend.create_semaphore(max_size)

    async def send(self, request: Request) -> AsyncResponse:
        conn = await self.connection_for_request(request)
        return await conn.send(request)

    async def connection_for_request(self, request) -> Connection:
        self.pool.
        async with self.pool:

