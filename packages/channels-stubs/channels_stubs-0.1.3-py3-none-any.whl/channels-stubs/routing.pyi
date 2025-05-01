from typing import Any, Sequence, TypeAlias

from asgiref.typing import ASGIReceiveCallable, ASGISendCallable
from django.urls.resolvers import URLPattern, URLResolver

from .consumer import _ChannelScope
from .utils import _ChannelApplication

def get_default_application() -> ProtocolTypeRouter: ...

class ProtocolTypeRouter:
    application_mapping: dict[str, _ChannelApplication]

    def __init__(self, application_mapping: dict[str, Any]) -> None: ...
    async def __call__(
        self,
        scope: _ChannelScope,
        receive: ASGIReceiveCallable,
        send: ASGISendCallable,
    ) -> None: ...

_IncludedURLConf: TypeAlias = tuple[
    Sequence[URLResolver | URLPattern], str | None, str | None
]

class URLRouter(_IncludedURLConf):
    _path_routing: bool = ...
    routes: list[URLPattern | URLResolver]

    def __init__(self, routes: list[URLPattern | URLResolver]) -> None: ...
    async def __call__(
        self,
        scope: _ChannelScope,
        receive: ASGIReceiveCallable,
        send: ASGISendCallable,
    ) -> None: ...

class ChannelNameRouter:
    application_mapping: dict[str, _ChannelApplication]

    def __init__(self, application_mapping: dict[str, _ChannelApplication]) -> None: ...
    async def __call__(
        self,
        scope: _ChannelScope,
        receive: ASGIReceiveCallable,
        send: ASGISendCallable,
    ) -> None: ...
