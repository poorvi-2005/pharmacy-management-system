from typing import List, Optional
from mysql.connector import Error
from ..database.db_connection import DatabaseConnection
from ..models.customer import Customer

class CustomerDAO:
    def __init__(self):
        self.db = DatabaseConnection()

    def add_customer(self, customer: Customer) -> bool:
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()
            
            query = """INSERT INTO customers (name, phone, email, address)
                      VALUES (%s, %s, %s, %s)"""
            values = (customer.name, customer.phone, customer.email, customer.address)
            
            cursor.execute(query, values)
            connection.commit()
            return True
        except Error as e:
            print(f"Error adding customer: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()
            
            query = "SELECT * FROM customers WHERE id = %s"
            cursor.execute(query, (customer_id,))
            
            result = cursor.fetchone()
            if result:
                return Customer(
                    id=result[0],
                    name=result[1],
                    phone=result[2],
                    email=result[3],
                    address=result[4]
                )
            return None
        except Error as e:
            print(f"Error retrieving customer: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def get_all_customers(self) -> List[Customer]:
        customers = []
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()
            
            query = "SELECT * FROM customers"
            cursor.execute(query)
            
            for row in cursor.fetchall():
                customer = Customer(
                    id=row[0],
                    name=row[1],
                    phone=row[2],
                    email=row[3],
                    address=row[4]
                )
                customers.append(customer)
        except Error as e:
            print(f"Error retrieving customers: {e}")
        finally:
            if cursor:
                cursor.close()
        return customers 

    def search_customers(self, search_term: str) -> List[Customer]:
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()
            
            query = """SELECT * FROM customers 
                      WHERE name LIKE %s OR phone LIKE %s OR email LIKE %s"""
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            
            customers = []
            for row in cursor.fetchall():
                customer = Customer(
                    id=row[0],
                    name=row[1],
                    phone=row[2],
                    email=row[3],
                    address=row[4]
                )
                customers.append(customer)
            return customers
        except Error as e:
            print(f"Error searching customers: {e}")
            return []
        finally:
            if cursor:
                cursor.close() 