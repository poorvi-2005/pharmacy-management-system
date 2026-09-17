from datetime import datetime
from typing import List
from .customer import Customer
from .medicine import Medicine

class BillItem:
    def __init__(self, medicine: Medicine, quantity: int):
        self.medicine = medicine
        self.quantity = quantity
        self.subtotal = medicine.price * quantity

class Bill:
    def __init__(self, id: int, customer: Customer, items: List[BillItem],
                 bill_date: datetime, discount: float = 0):
        self.id = id
        self.customer = customer
        self.items = items
        self.bill_date = bill_date
        self.discount = discount
        self.total = sum(item.subtotal for item in items)
        self.final_amount = self.total * (1 - discount/100) 