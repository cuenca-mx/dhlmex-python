from typing import ClassVar


class Resource:
    _client: ClassVar['cepmex.Client']  # type: ignore
