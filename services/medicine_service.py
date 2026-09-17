from typing import List, Optional
from datetime import datetime, timedelta
from ..models.medicine import Medicine
from ..repositories.medicine_repository import MedicineRepository
from .base_service import BaseService
from ..exceptions import ValidationError, NotFoundException

class MedicineService(BaseService[Medicine]):
    def __init__(self):
        super().__init__(MedicineRepository())

    def create_medicine(self, medicine_data: dict) -> Medicine:
        self._validate_medicine_data(medicine_data)
        
        medicine = Medicine(
            id=0,
            name=medicine_data['name'],
            batch_number=medicine_data['batch_number'],
            expiry_date=datetime.strptime(medicine_data['expiry_date'], '%Y-%m-%d'),
            quantity=int(medicine_data['quantity']),
            price=float(medicine_data['price']),
            manufacturer=medicine_data['manufacturer'],
            category=medicine_data.get('category')
        )
        
        medicine_id = self.repository.create(medicine)
        if not medicine_id:
            raise ValidationError("Failed to create medicine")
        
        medicine.id = medicine_id
        return medicine

    def update_medicine(self, id: int, medicine_data: dict) -> Medicine:
        existing_medicine = self.get_medicine_by_id(id)
        if not existing_medicine:
            raise NotFoundException(f"Medicine with ID {id} not found")

        self._validate_medicine_data(medicine_data)
        
        for key, value in medicine_data.items():
            if hasattr(existing_medicine, key):
                if key == 'expiry_date':
                    value = datetime.strptime(value, '%Y-%m-%d')
                setattr(existing_medicine, key, value)

        if not self.repository.update(existing_medicine):
            raise ValidationError("Failed to update medicine")
        
        return existing_medicine

    def delete_medicine(self, id: int) -> bool:
        if not self.get_medicine_by_id(id):
            raise NotFoundException(f"Medicine with ID {id} not found")
        return self.repository.delete(id)

    def get_medicine_by_id(self, id: int) -> Optional[Medicine]:
        return self.repository.find_by_id(id)

    def get_all_medicines(self) -> List[Medicine]:
        return self.repository.find_all()

    def search_medicines(self, filters: dict) -> List[Medicine]:
        return self.repository.search(filters)

    def get_low_stock_medicines(self, threshold: int = 10) -> List[Medicine]:
        return self.repository.search({'low_stock': threshold})

    def get_expiring_medicines(self, days: int = 30) -> List[Medicine]:
        expiry_date = datetime.now() + timedelta(days=days)
        return self.repository.search({'expiring_before': expiry_date})

    def _validate_medicine_data(self, data: dict):
        required_fields = ['name', 'batch_number', 'expiry_date', 'quantity', 'price', 'manufacturer']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")

        try:
            expiry_date = datetime.strptime(data['expiry_date'], '%Y-%m-%d')
            if expiry_date < datetime.now():
                raise ValidationError("Expiry date cannot be in the past")
        except ValueError:
            raise ValidationError("Invalid expiry date format. Use YYYY-MM-DD")

        try:
            quantity = int(data['quantity'])
            if quantity < 0:
                raise ValidationError("Quantity cannot be negative")
        except ValueError:
            raise ValidationError("Invalid quantity value")

        try:
            price = float(data['price'])
            if price <= 0:
                raise ValidationError("Price must be greater than zero")
        except ValueError:
            raise ValidationError("Invalid price value") 