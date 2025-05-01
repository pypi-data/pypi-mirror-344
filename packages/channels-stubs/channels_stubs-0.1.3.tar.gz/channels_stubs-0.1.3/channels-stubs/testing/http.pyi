from typing import Iterable, Literal, Optional, Tuple, TypedDict

from channels.testing.application import ApplicationCommunicator
from channels.utils import _ChannelApplication

# HTTP test-specific response type
class _HTTPTestResponse(TypedDict, total=False):
    status: int
    headers: Iterable[Tuple[bytes, bytes]]
    body: bytes

class _HTTPTestScope(TypedDict, total=False):
    type: Literal["http"]
    http_version: str
    method: str
    scheme: str
    path: str
    raw_path: bytes
    query_string: bytes
    root_path: str
    headers: Iterable[Tuple[bytes, bytes]] | None
    client: Optional[Tuple[str, int]]
    server: Optional[Tuple[str, Optional[int]]]

class HttpCommunicator(ApplicationCommunicator):
    scope: _HTTPTestScope
    body: bytes
    sent_request: bool

    def __init__(
        self,
        application: _ChannelApplication,
        method: str,
        path: str,
        body: bytes = ...,
        headers: Iterable[Tuple[bytes, bytes]] | None = ...,
    ) -> None: ...
    async def get_response(self, timeout: float = ...) -> _HTTPTestResponse: ...
