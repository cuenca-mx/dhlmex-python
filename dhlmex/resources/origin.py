from dataclasses import dataclass


@dataclass
class Origin:
    company: str
    contact: str
    mail: str
    phone: str
    address1: str
    postal_code: str
    neighborhood: str
    city: str
    state: str
