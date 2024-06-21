# employee_management.py
import mysql.connector
from mysql.connector import Error
from config import RDS_HOST, RDS_PORT, RDS_USER, RDS_PASSWORD, RDS_DB
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


class EmployeeRecordManagement:
    def __init__(self):
        self.conn = self.create_connection()
        self.cursor = self.conn.cursor()

    def create_connection(self):
        """Create a database connection to the AWS RDS MySQL database"""
        try:
            connection = mysql.connector.connect(
                host='sip3.cjuo44okojjd.ap-south-1.rds.amazonaws.com',
                port=3306,
                user='root',
                password='BCAH5-2024',
                database='emp1'
            )
            if connection.is_connected():
                print("Connected to AWS RDS MySQL instance")
                return connection
        except Error as e:
            print(f"Error: {e}")
            return None

    def add_employee(self, name, contact_info, job_title, department, joining_date):
        self.cursor.execute("""
            INSERT INTO employees (name, contact_info, job_title, department, joining_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, contact_info, job_title, department, joining_date))
        self.conn.commit()

    def edit_employee(self, employee_id, name, contact_info, job_title, department, joining_date):
        self.cursor.execute("""
            UPDATE employees
            SET name=%s, contact_info=%s, job_title=%s, department=%s, joining_date=%s
            WHERE employee_id=%s
        """, (name, contact_info, job_title, department, joining_date, employee_id))
        self.conn.commit()

    def delete_employee(self, employee_id):
        self.cursor.execute("DELETE FROM employees WHERE employee_id=%s", (employee_id,))
        self.conn.commit()

    def view_employees(self):
        self.cursor.execute("SELECT * FROM employees")
        return self.cursor.fetchall()


class EmployeeManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("800x600")

        #  background image
        self.background_image = Image.open("Background.jpeg")
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        self.db = EmployeeRecordManagement()

        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.root,
                                 columns=("ID", "Name", "Contact", "Job Title", "Department", "Joining Date"),
                                 show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Contact", text="Contact")
        self.tree.heading("Job Title", text="Job Title")
        self.tree.heading("Department", text="Department")
        self.tree.heading("Joining Date", text="Joining Date")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.load_data()

        self.form_frame = tk.Frame(self.root, bg='white')
        self.form_frame.pack(pady=20)

        tk.Label(self.form_frame, text="Name", bg='white').grid(row=0, column=0)
        self.name_entry = tk.Entry(self.form_frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self.form_frame, text="Contact Info", bg='white').grid(row=1, column=0)
        self.contact_entry = tk.Entry(self.form_frame)
        self.contact_entry.grid(row=1, column=1)

        tk.Label(self.form_frame, text="Job Title", bg='white').grid(row=2, column=0)
        self.job_title_entry = tk.Entry(self.form_frame)
        self.job_title_entry.grid(row=2, column=1)

        tk.Label(self.form_frame, text="Department", bg='white').grid(row=3, column=0)
        self.department_entry = tk.Entry(self.form_frame)
        self.department_entry.grid(row=3, column=1)

        tk.Label(self.form_frame, text="Joining Date (YYYY-MM-DD)", bg='white').grid(row=4, column=0)
        self.joining_date_entry = tk.Entry(self.form_frame)
        self.joining_date_entry.grid(row=4, column=1)

        self.add_button = tk.Button(self.form_frame, text="Add Employee", command=self.add_employee, bg='lightblue')
        self.add_button.grid(row=5, column=0, pady=10)

        self.edit_button = tk.Button(self.form_frame, text="Edit Employee", command=self.edit_employee, bg='lightblue')
        self.edit_button.grid(row=5, column=1, pady=10)

        self.delete_button = tk.Button(self.form_frame, text="Delete Employee", command=self.delete_employee,
                                       bg='lightblue')
        self.delete_button.grid(row=5, column=2, pady=10)

    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.db.view_employees():
            self.tree.insert("", tk.END, values=row)

    def add_employee(self):
        name = self.name_entry.get()
        contact_info = self.contact_entry.get()
        job_title = self.job_title_entry.get()
        department = self.department_entry.get()
        joining_date = self.joining_date_entry.get()
        self.db.add_employee(name, contact_info, job_title, department, joining_date)
        self.load_data()
        messagebox.showinfo("Success", "Employee added successfully")

    def edit_employee(self):
        selected_item = self.tree.selection()[0]
        employee_id = self.tree.item(selected_item)['values'][0]
        name = self.name_entry.get()
        contact_info = self.contact_entry.get()
        job_title = self.job_title_entry.get()
        department = self.department_entry.get()
        joining_date = self.joining_date_entry.get()
        self.db.edit_employee(employee_id, name, contact_info, job_title, department, joining_date)
        self.load_data()
        messagebox.showinfo("Success", "Employee details updated successfully")

    def delete_employee(self):
        selected_item = self.tree.selection()[0]
        employee_id = self.tree.item(selected_item)['values'][0]
        self.db.delete_employee(employee_id)
        self.load_data()
        messagebox.showinfo("Success", "Employee deleted successfully")


if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementApp(root)
    root.mainloop()
