from typing import ClassVar


class Resource:
    _client: ClassVar["dhlmex.Client"]  # type: ignore
