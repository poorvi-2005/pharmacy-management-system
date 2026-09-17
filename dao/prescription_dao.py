from typing import List, Optional
from mysql.connector import Error
from ..database.db_connection import DatabaseConnection
from ..models.prescription import Prescription
from ..models.medicine import Medicine
from ..dao.customer_dao import CustomerDAO
from ..dao.medicine_dao import MedicineDAO

class PrescriptionDAO:
    def __init__(self):
        self.db = DatabaseConnection()
        self.customer_dao = CustomerDAO()
        self.medicine_dao = MedicineDAO()

    def add_prescription(self, prescription: Prescription) -> bool:
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()
            
            # Insert prescription
            query = """INSERT INTO prescriptions 
                      (customer_id, doctor_name, prescription_date, notes)
                      VALUES (%s, %s, %s, %s)"""
            values = (prescription.customer.id, prescription.doctor_name,
                     prescription.prescription_date, prescription.notes)
            
            cursor.execute(query, values)
            prescription_id = cursor.lastrowid
            
            # Insert prescription medicines
            for medicine in prescription.medicines:
                query = """INSERT INTO prescription_medicines 
                          (prescription_id, medicine_id, quantity)
                          VALUES (%s, %s, %s)"""
                cursor.execute(query, (prescription_id, medicine.id, medicine.quantity))
            
            connection.commit()
            return True
        except Error as e:
            print(f"Error adding prescription: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

    def get_prescription_by_id(self, prescription_id: int) -> Optional[Prescription]:
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()
            
            # Get prescription details
            query = "SELECT * FROM prescriptions WHERE id = %s"
            cursor.execute(query, (prescription_id,))
            
            result = cursor.fetchone()
            if not result:
                return None
                
            customer = self.customer_dao.get_customer_by_id(result[1])
            
            # Get prescription medicines
            query = """SELECT m.*, pm.quantity 
                      FROM medicines m 
                      JOIN prescription_medicines pm ON m.id = pm.medicine_id 
                      WHERE pm.prescription_id = %s"""
            cursor.execute(query, (prescription_id,))
            
            medicines = []
            for row in cursor.fetchall():
                medicine = Medicine(
                    id=row[0],
                    name=row[1],
                    batch_number=row[2],
                    expiry_date=row[3],
                    quantity=row[7],  # Using quantity from prescription_medicines
                    price=row[5],
                    manufacturer=row[6]
                )
                medicines.append(medicine)
            
            return Prescription(
                id=result[0],
                customer=customer,
                doctor_name=result[2],
                prescription_date=result[3],
                medicines=medicines,
                notes=result[4]
            )
        except Error as e:
            print(f"Error retrieving prescription: {e}")
            return None
        finally:
            if cursor:
                cursor.close() 

    def search_prescriptions(self, filters: dict) -> List[Prescription]:
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()
            
            query = """SELECT p.*, c.name as customer_name 
                      FROM prescriptions p
                      JOIN customers c ON p.customer_id = c.id
                      WHERE 1=1"""
            params = []
            
            if 'customer_name' in filters:
                query += " AND c.name LIKE %s"
                params.append(f"%{filters['customer_name']}%")
            
            if 'doctor_name' in filters:
                query += " AND p.doctor_name LIKE %s"
                params.append(f"%{filters['doctor_name']}%")
            
            if 'prescription_date' in filters:
                query += " AND DATE(p.prescription_date) = %s"
                params.append(filters['prescription_date'])
            
            cursor.execute(query, tuple(params))
            
            prescriptions = []
            for row in cursor.fetchall():
                prescription = self._create_prescription_from_row(row)
                prescriptions.append(prescription)
            return prescriptions
        except Error as e:
            print(f"Error searching prescriptions: {e}")
            return []
        finally:
            if cursor:
                cursor.close() 