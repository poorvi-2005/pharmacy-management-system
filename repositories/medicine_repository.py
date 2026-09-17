from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from ..models.medicine import Medicine
from .base_repository import BaseRepository

class MedicineRepository(BaseRepository[Medicine]):
    def create(self, medicine: Medicine) -> Optional[int]:
        query = """
            INSERT INTO medicines (
                name, batch_number, expiry_date, quantity, 
                price, manufacturer, category, is_active
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            medicine.name, medicine.batch_number, medicine.expiry_date,
            medicine.quantity, medicine.price, medicine.manufacturer,
            medicine.category, medicine.is_active
        )
        return self.execute_query(query, params)

    def update(self, medicine: Medicine) -> bool:
        query = """
            UPDATE medicines 
            SET name=%s, batch_number=%s, expiry_date=%s, quantity=%s,
                price=%s, manufacturer=%s, category=%s, is_active=%s,
                updated_at=CURRENT_TIMESTAMP
            WHERE id=%s
        """
        params = (
            medicine.name, medicine.batch_number, medicine.expiry_date,
            medicine.quantity, medicine.price, medicine.manufacturer,
            medicine.category, medicine.is_active, medicine.id
        )
        return bool(self.execute_query(query, params))

    def delete(self, id: int) -> bool:
        query = "UPDATE medicines SET is_active=FALSE WHERE id=%s"
        return bool(self.execute_query(query, (id,)))

    def find_by_id(self, id: int) -> Optional[Medicine]:
        query = "SELECT * FROM medicines WHERE id=%s AND is_active=TRUE"
        row = self.fetch_one(query, (id,))
        return self._create_medicine_from_row(row) if row else None

    def find_all(self) -> List[Medicine]:
        query = "SELECT * FROM medicines WHERE is_active=TRUE ORDER BY name"
        rows = self.fetch_all(query)
        return [self._create_medicine_from_row(row) for row in rows]

    def search(self, filters: dict) -> List[Medicine]:
        query = "SELECT * FROM medicines WHERE is_active=TRUE"
        params = []

        if 'name' in filters:
            query += " AND name LIKE %s"
            params.append(f"%{filters['name']}%")

        if 'manufacturer' in filters:
            query += " AND manufacturer LIKE %s"
            params.append(f"%{filters['manufacturer']}%")

        if 'category' in filters:
            query += " AND category = %s"
            params.append(filters['category'])

        if 'expiring_before' in filters:
            query += " AND expiry_date <= %s"
            params.append(filters['expiring_before'])

        if 'low_stock' in filters:
            query += " AND quantity <= %s"
            params.append(filters['low_stock'])

        query += " ORDER BY name"
        rows = self.fetch_all(query, tuple(params))
        return [self._create_medicine_from_row(row) for row in rows]

    def _create_medicine_from_row(self, row: tuple) -> Medicine:
        return Medicine(
            id=row[0],
            name=row[1],
            batch_number=row[2],
            expiry_date=row[3],
            quantity=row[4],
            price=Decimal(str(row[5])),
            manufacturer=row[6],
            category=row[7]
        ) 