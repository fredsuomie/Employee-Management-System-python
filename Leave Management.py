import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class LeaveManagement:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='sip3.cjuo44okojjd.ap-south-1.rds.amazonaws.com',
            port=3306,
            user='root',
            password='BCAH5-2024',
            database="emp1"
        )
        self.cursor = self.conn.cursor()

    def apply_leave(self, employee_id, leave_type, start_date, end_date, reason):
        self.cursor.execute("""
            INSERT INTO leave_requests (employee_id, leave_type, start_date, end_date, reason, status)
            VALUES (%s, %s, %s, %s, %s, 'Pending')
        """, (employee_id, leave_type, start_date, end_date, reason))
        self.conn.commit()

    def approve_leave(self, request_id):
        self.cursor.execute("""
            UPDATE leave_requests SET status='Approved' WHERE request_id=%s
        """, (request_id,))
        self.conn.commit()

    def reject_leave(self, request_id):
        self.cursor.execute("""
            UPDATE leave_requests SET status='Rejected' WHERE request_id=%s
        """, (request_id,))
        self.conn.commit()

    def get_leave_requests(self):
        self.cursor.execute("""
            SELECT lr.request_id, e.name, lr.leave_type, lr.start_date, lr.end_date, lr.reason, lr.status 
            FROM leave_requests lr JOIN employees e ON lr.employee_id = e.employee_id
        """)
        return self.cursor.fetchall()

class LeaveManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Leave Management System")
        self.root.geometry("800x600")

        # Load background image
        self.background_image = Image.open("Background.jpeg")
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        self.db = LeaveManagement()

        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.root, columns=(
            "Request ID", "Employee Name", "Leave Type", "Start Date", "End Date", "Reason", "Status"), show='headings')
        self.tree.heading("Request ID", text="Request ID")
        self.tree.heading("Employee Name", text="Employee Name")
        self.tree.heading("Leave Type", text="Leave Type")
        self.tree.heading("Start Date", text="Start Date")
        self.tree.heading("End Date", text="End Date")
        self.tree.heading("Reason", text="Reason")
        self.tree.heading("Status", text="Status")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.load_data()

        self.form_frame = tk.Frame(self.root, bg='white')
        self.form_frame.pack(pady=20)

        tk.Label(self.form_frame, text="Employee ID", bg='white').grid(row=0, column=0)
        self.employee_id_entry = tk.Entry(self.form_frame)
        self.employee_id_entry.grid(row=0, column=1)

        tk.Label(self.form_frame, text="Leave Type", bg='white').grid(row=1, column=0)
        self.leave_type_entry = tk.Entry(self.form_frame)
        self.leave_type_entry.grid(row=1, column=1)

        tk.Label(self.form_frame, text="Start Date (YYYY-MM-DD)", bg='white').grid(row=2, column=0)
        self.start_date_entry = tk.Entry(self.form_frame)
        self.start_date_entry.grid(row=2, column=1)

        tk.Label(self.form_frame, text="End Date (YYYY-MM-DD)", bg='white').grid(row=3, column=0)
        self.end_date_entry = tk.Entry(self.form_frame)
        self.end_date_entry.grid(row=3, column=1)

        tk.Label(self.form_frame, text="Reason", bg='white').grid(row=4, column=0)
        self.reason_entry = tk.Entry(self.form_frame)
        self.reason_entry.grid(row=4, column=1)

        self.apply_button = tk.Button(self.form_frame, text="Apply for Leave", command=self.apply_leave, bg='lightblue')
        self.apply_button.grid(row=5, column=0, pady=10)

        self.approve_button = tk.Button(self.form_frame, text="Approve Leave", command=self.approve_leave, bg='lightgreen')
        self.approve_button.grid(row=5, column=1, pady=10)

        self.reject_button = tk.Button(self.form_frame, text="Reject Leave", command=self.reject_leave, bg='red')
        self.reject_button.grid(row=5, column=2, pady=10)

    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.db.get_leave_requests():
            self.tree.insert("", tk.END, values=row)

    def apply_leave(self):
        employee_id = self.employee_id_entry.get()
        leave_type = self.leave_type_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        reason = self.reason_entry.get()
        self.db.apply_leave(employee_id, leave_type, start_date, end_date, reason)
        self.load_data()
        messagebox.showinfo("Success", "Leave request submitted successfully")

    def approve_leave(self):
        selected_item = self.tree.selection()[0]
        request_id = self.tree.item(selected_item)['values'][0]
        self.db.approve_leave(request_id)
        self.load_data()
        messagebox.showinfo("Success", "Leave request approved")

    def reject_leave(self):
        selected_item = self.tree.selection()[0]
        request_id = self.tree.item(selected_item)['values'][0]
        self.db.reject_leave(request_id)
        self.load_data()
        messagebox.showinfo("Success", "Leave request rejected")

if __name__ == "__main__":
    root = tk.Tk()
    app = LeaveManagementApp(root)
    root.mainloop()
