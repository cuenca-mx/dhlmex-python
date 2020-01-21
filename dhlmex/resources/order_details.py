from dataclasses import dataclass


@dataclass
class OrderDetails:
    description: str
    content: str

    def __post_init__(self):
        self.description = self.description[:35]
        self.content = self.content[:25]
