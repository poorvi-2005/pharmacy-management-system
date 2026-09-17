from typing import List, Optional
from datetime import datetime
from mysql.connector import Error
from ..database.db_connection import DatabaseConnection
from ..models.bill import Bill, BillItem
from ..dao.customer_dao import CustomerDAO
from ..dao.medicine_dao import MedicineDAO

class BillDAO:
    def __init__(self):
        self.db = DatabaseConnection()
        self.customer_dao = CustomerDAO()
        self.medicine_dao = MedicineDAO()

    def create_bill(self, bill: Bill) -> bool:
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()
            
            # Insert bill
            query = """INSERT INTO bills 
                      (customer_id, bill_date, discount, total_amount, final_amount)
                      VALUES (%s, %s, %s, %s, %s)"""
            values = (bill.customer.id, bill.bill_date, bill.discount,
                     bill.total, bill.final_amount)
            
            cursor.execute(query, values)
            bill_id = cursor.lastrowid
            
            # Insert bill items
            for item in bill.items:
                query = """INSERT INTO bill_items 
                          (bill_id, medicine_id, quantity, unit_price, subtotal)
                          VALUES (%s, %s, %s, %s, %s)"""
                values = (bill_id, item.medicine.id, item.quantity,
                         item.medicine.price, item.subtotal)
                cursor.execute(query, values)
                
                # Update medicine stock
                query = """UPDATE medicines 
                          SET quantity = quantity - %s 
                          WHERE id = %s"""
                cursor.execute(query, (item.quantity, item.medicine.id))
            
            connection.commit()
            return True
        except Error as e:
            print(f"Error creating bill: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

    def get_bill_by_id(self, bill_id: int) -> Optional[Bill]:
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()
            
            # Get bill details
            query = "SELECT * FROM bills WHERE id = %s"
            cursor.execute(query, (bill_id,))
            
            result = cursor.fetchone()
            if not result:
                return None
                
            customer = self.customer_dao.get_customer_by_id(result[1])
            
            # Get bill items
            query = """SELECT m.*, bi.quantity, bi.unit_price, bi.subtotal 
                      FROM medicines m 
                      JOIN bill_items bi ON m.id = bi.medicine_id 
                      WHERE bi.bill_id = %s"""
            cursor.execute(query, (bill_id,))
            
            items = []
            for row in cursor.fetchall():
                medicine = Medicine(
                    id=row[0],
                    name=row[1],
                    batch_number=row[2],
                    expiry_date=row[3],
                    quantity=row[8],  # Using quantity from bill_items
                    price=row[9],     # Using unit_price from bill_items
                    manufacturer=row[6]
                )
                item = BillItem(medicine=medicine, quantity=row[8])
                items.append(item)
            
            return Bill(
                id=result[0],
                customer=customer,
                items=items,
                bill_date=result[2],
                discount=result[3]
            )
        except Error as e:
            print(f"Error retrieving bill: {e}")
            return None
        finally:
            if cursor:
                cursor.close() 

    def search_bills(self, filters: dict) -> List[Bill]:
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()
            
            query = """SELECT b.*, c.name as customer_name 
                      FROM bills b
                      JOIN customers c ON b.customer_id = c.id
                      WHERE 1=1"""
            params = []
            
            if 'customer_name' in filters:
                query += " AND c.name LIKE %s"
                params.append(f"%{filters['customer_name']}%")
            
            if 'bill_date' in filters:
                query += " AND DATE(b.bill_date) = %s"
                params.append(filters['bill_date'])
            
            if 'min_amount' in filters:
                query += " AND b.final_amount >= %s"
                params.append(filters['min_amount'])
            
            if 'max_amount' in filters:
                query += " AND b.final_amount <= %s"
                params.append(filters['max_amount'])
            
            query += " ORDER BY b.bill_date DESC"
            
            cursor.execute(query, tuple(params))
            
            bills = []
            for row in cursor.fetchall():
                bill = self._create_bill_from_row(row)
                bills.append(bill)
            return bills
        except Error as e:
            print(f"Error searching bills: {e}")
            return []
        finally:
            if cursor:
                cursor.close() 