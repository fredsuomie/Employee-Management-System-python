import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class PayrollManagement:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='sip3.cjuo44okojjd.ap-south-1.rds.amazonaws.com',
            port=3306,
            user='root',
            password='BCAH5-2024',
            database="emp1"
        )
        self.cursor = self.conn.cursor()

    def calculate_net_salary(self, basic_salary, deductions, bonuses):
        try:
            basic_salary = float(basic_salary)
            deductions = float(deductions)
            bonuses = float(bonuses)
            return basic_salary - deductions + bonuses
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values for salary, deductions, and bonuses")
            return None

    def add_payroll_record(self, employee_id, basic_salary, deductions, bonuses, pay_date):
        net_salary = self.calculate_net_salary(basic_salary, deductions, bonuses)
        if net_salary is not None:
            self.cursor.execute("""
                INSERT INTO payroll (employee_id, basic_salary, deductions, bonuses, net_salary, pay_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (employee_id, basic_salary, deductions, bonuses, net_salary, pay_date))
            self.conn.commit()
            messagebox.showinfo("Success", "Payroll record added successfully")

    def get_payroll_records(self):
        self.cursor.execute("SELECT * FROM payroll")
        return self.cursor.fetchall()

class PayrollManagementApp:
    def __init__(self, root, payroll_management):
        self.payroll_management = payroll_management

        self.root = root
        self.root.title("Payroll Management")

        # Load and set the background image
        self.background_image = Image.open("Background.jpeg")  # Ensure this image path is correct
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.background_label = Label(self.root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        # Create a frame to hold the widgets
        self.frame = Frame(root, bg='white')
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=0.8, relheight=0.8)

        # Form fields
        self.employee_id_label = Label(self.frame, text="Employee ID", bg='white')
        self.employee_id_label.grid(row=0, column=0, pady=10, padx=10)
        self.employee_id_entry = Entry(self.frame)
        self.employee_id_entry.grid(row=0, column=1, pady=10, padx=10)

        self.basic_salary_label = Label(self.frame, text="Basic Salary", bg='white')
        self.basic_salary_label.grid(row=1, column=0, pady=10, padx=10)
        self.basic_salary_entry = Entry(self.frame)
        self.basic_salary_entry.grid(row=1, column=1, pady=10, padx=10)

        self.deductions_label = Label(self.frame, text="Deductions", bg='white')
        self.deductions_label.grid(row=2, column=0, pady=10, padx=10)
        self.deductions_entry = Entry(self.frame)
        self.deductions_entry.grid(row=2, column=1, pady=10, padx=10)

        self.bonuses_label = Label(self.frame, text="Bonuses", bg='white')
        self.bonuses_label.grid(row=3, column=0, pady=10, padx=10)
        self.bonuses_entry = Entry(self.frame)
        self.bonuses_entry.grid(row=3, column=1, pady=10, padx=10)

        self.pay_date_label = Label(self.frame, text="Pay Date (YYYY-MM-DD)", bg='white')
        self.pay_date_label.grid(row=4, column=0, pady=10, padx=10)
        self.pay_date_entry = Entry(self.frame)
        self.pay_date_entry.grid(row=4, column=1, pady=10, padx=10)

        self.add_button = Button(self.frame, text="Add Payroll Record", command=self.add_payroll_record, bg='lightblue')
        self.add_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Create data table for payroll records
        self.tree = ttk.Treeview(self.frame, columns=(
            "payroll_id", "employee_id", "basic_salary", "deductions", "bonuses", "net_salary", "pay_date"),
                                 show='headings')
        self.tree.heading("payroll_id", text="Payroll ID")
        self.tree.heading("employee_id", text="Employee ID")
        self.tree.heading("basic_salary", text="Basic Salary")
        self.tree.heading("deductions", text="Deductions")
        self.tree.heading("bonuses", text="Bonuses")
        self.tree.heading("net_salary", text="Net Salary")
        self.tree.heading("pay_date", text="Pay Date")
        self.tree.grid(row=6, column=0, columnspan=2, pady=10)

        self.refresh_payroll_records()

    def add_payroll_record(self):
        employee_id = self.employee_id_entry.get()
        basic_salary = self.basic_salary_entry.get()
        deductions = self.deductions_entry.get()
        bonuses = self.bonuses_entry.get()
        pay_date = self.pay_date_entry.get()

        self.payroll_management.add_payroll_record(employee_id, basic_salary, deductions, bonuses, pay_date)
        self.refresh_payroll_records()

    def refresh_payroll_records(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        payroll_records = self.payroll_management.get_payroll_records()
        for record in payroll_records:
            self.tree.insert('', 'end', values=record)

if __name__ == "__main__":
    root = Tk()
    payroll_management = PayrollManagement()
    payroll_management_app = PayrollManagementApp(root, payroll_management)
    root.mainloop()
