from beanie import Document

class Address(Document):
    name: str
    contactNumber: str
    street: str
    city: str
    state: str
    landmark: str
    zipcode: int
    email: str
