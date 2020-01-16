from dataclasses import dataclass


@dataclass
class OrderDetails:
    description: str
    content: str
