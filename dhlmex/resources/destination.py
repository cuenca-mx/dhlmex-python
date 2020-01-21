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

    def __post_init__(self):
        self.company = self.company[:60]
        self.contact = self.contact[:35]
        self.email = self.email[:40]
        self.phone = self.phone[:15]
        self.address1 = self.address1[:44]
        self.postal_code = self.postal_code[:5]
        self.neighborhood = self.neighborhood[:35]
        self.city = self.city[:35]
        self.state = self.state[:35]
