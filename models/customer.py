class Customer:
    def __init__(self, id: int, name: str, phone: str, email: str, address: str):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def __str__(self):
        return f"{self.name} ({self.phone})" 