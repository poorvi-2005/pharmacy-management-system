from datetime import datetime
from decimal import Decimal
from .base import BaseModel

class Medicine(BaseModel):
    def __init__(self, id: int, name: str, batch_number: str, expiry_date: datetime,
                 quantity: int, price: Decimal, manufacturer: str, category: str = None):
        self.id = id
        self.name = name
        self.batch_number = batch_number
        self.expiry_date = expiry_date
        self.quantity = quantity
        self.price = price
        self.manufacturer = manufacturer
        self.category = category
        self.is_active = True

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            'id': self.id,
            'name': self.name,
            'batch_number': self.batch_number,
            'expiry_date': self.expiry_date.isoformat(),
            'quantity': self.quantity,
            'price': str(self.price),
            'manufacturer': self.manufacturer,
            'category': self.category,
            'is_active': self.is_active
        }

    def __str__(self):
        return f"{self.name} (Batch: {self.batch_number})" 