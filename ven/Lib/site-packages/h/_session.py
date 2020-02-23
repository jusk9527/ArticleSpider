import typing


class BaseSession:
    pass


class SyncSession(BaseSession):
    """Synchronous HTTP session"""
    def request(self, method: str, url: str, *, headers=None, timeout=None):
        pass

    def close(self) -> None:
        pass


class AsyncSession(BaseSession):
    """Asynchronous HTTP session"""
    async def request(self, method: str, url: str, *, headers=None, timeout=None):
        pass

    async def close(self) -> None:
        pass


class SessionManager:
    """Simple class which determines if using the async or synchronous mode"""
    def __init__(self, base_url: str=None, ):
        self._session: typing.Optional[typing.Union[SyncSession, AsyncSession]] = None

    async def __aenter__(self) -> AsyncSession:
        self._session = AsyncSession()
        return self._session

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._session and isinstance(self._session, AsyncSession):
            await self._session.close()

    def __enter__(self) -> SyncSession:
        self._session = SyncSession()
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._session and isinstance(self._session, SyncSession):
            self._session.close()
