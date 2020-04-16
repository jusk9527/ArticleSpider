from h.ttp.models import Request, AsyncResponse


class Connection:
    async def send(self, request: Request) -> AsyncResponse:
        pass
