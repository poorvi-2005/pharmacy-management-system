from datetime import date
from typing import List
from .customer import Customer
from .medicine import Medicine

class Prescription:
    def __init__(self, id: int, customer: Customer, doctor_name: str,
                 prescription_date: date, medicines: List[Medicine], notes: str):
        self.id = id
        self.customer = customer
        self.doctor_name = doctor_name
        self.prescription_date = prescription_date
        self.medicines = medicines
        self.notes = notes

    def __str__(self):
        return f"Prescription #{self.id} - Dr. {self.doctor_name}" 