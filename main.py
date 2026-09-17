from datetime import datetime
from dao.medicine_dao import MedicineDAO
from dao.customer_dao import CustomerDAO
from dao.prescription_dao import PrescriptionDAO
from dao.bill_dao import BillDAO
from models.medicine import Medicine
from models.customer import Customer
from models.prescription import Prescription
from models.bill import Bill, BillItem

class PharmacyManagementSystem:
    def __init__(self):
        self.medicine_dao = MedicineDAO()
        self.customer_dao = CustomerDAO()
        self.prescription_dao = PrescriptionDAO()
        self.bill_dao = BillDAO()

    def display_menu(self):
        print("\n=== Pharmacy Management System ===")
        print("1. Medicine Management")
        print("2. Customer Management")
        print("3. Prescription Management")
        print("4. Billing")
        print("5. Reports")
        print("6. Exit")

    def display_medicine_menu(self):
        print("\n=== Medicine Management ===")
        print("1. Add New Medicine")
        print("2. Update Medicine")
        print("3. Delete Medicine")
        print("4. View All Medicines")
        print("5. Check Low Stock")
        print("6. Back to Main Menu")

    def display_customer_menu(self):
        print("\n=== Customer Management ===")
        print("1. Add New Customer")
        print("2. View Customer Details")
        print("3. View All Customers")
        print("4. Back to Main Menu")

    def display_prescription_menu(self):
        print("\n=== Prescription Management ===")
        print("1. Create New Prescription")
        print("2. View Prescription Details")
        print("3. Back to Main Menu")

    def display_billing_menu(self):
        print("\n=== Billing ===")
        print("1. Create New Bill")
        print("2. View Bill Details")
        print("3. Back to Main Menu")

    def run(self):
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-6): ")

            if choice == '1':
                self.medicine_menu()
            elif choice == '2':
                self.customer_menu()
            elif choice == '3':
                self.prescription_menu()
            elif choice == '4':
                self.billing_menu()
            elif choice == '5':
                self.generate_reports()
            elif choice == '6':
                print("Thank you for using Pharmacy Management System!")
                break
            else:
                print("Invalid choice. Please try again.")

    def create_bill(self):
        print("\n=== Create New Bill ===")
        
        # Get customer
        customer_id = int(input("Enter customer ID: "))
        customer = self.customer_dao.get_customer_by_id(customer_id)
        if not customer:
            print("Customer not found.")
            return

        items = []
        while True:
            medicine_id = input("\nEnter medicine ID (or press Enter to finish): ")
            if not medicine_id:
                break

            medicine = self.medicine_dao.get_medicine_by_id(int(medicine_id))
            if not medicine:
                print("Medicine not found.")
                continue

            quantity = int(input("Enter quantity: "))
            if quantity > medicine.quantity:
                print("Insufficient stock!")
                continue

            items.append(BillItem(medicine=medicine, quantity=quantity))

        if not items:
            print("No items added to bill.")
            return

        discount = float(input("\nEnter discount percentage (0-100): "))
        
        bill = Bill(
            id=0,  # Will be assigned by database
            customer=customer,
            items=items,
            bill_date=datetime.now(),
            discount=discount
        )

        if self.bill_dao.create_bill(bill):
            print("\nBill created successfully!")
            self.print_bill(bill)
        else:
            print("Failed to create bill.")

    def print_bill(self, bill: Bill):
        print("\n" + "="*50)
        print("                 PHARMACY BILL") 