from dataclasses import dataclass


@dataclass
class Destination:
    company: str
    contact: str
    email: str
    phone: str
    address1: str
    postal_code: str
    neighborhood: str
    city: str
    state: str
