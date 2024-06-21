import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import hashlib

class UserManagement:
    def __init__(self):
        # Connect to the AWS RDS instance
        self.conn = mysql.connector.connect(
            host='sip3.cjuo44okojjd.ap-south-1.rds.amazonaws.com',
            port=3306,
            user='root',
            password='BCAH5-2024',
            database='emp1'
        )
        self.cursor = self.conn.cursor()
        self.create_tables()

        self.root = tk.Tk()
        self.root.title("User Management System")

        # Create a canvas to set the background
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Load background image
        try:
            self.background_image = Image.open("Background.jpeg")
            self.background_photo = ImageTk.PhotoImage(self.background_image)
            self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load background image: {e}")

        # Frame to contain the widgets
        self.frame = tk.Frame(self.root, bg="white", bd=2)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.username_label = tk.Label(self.frame, text="Username")
        self.username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = tk.Label(self.frame, text="Password")
        self.password_label.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.role_label = tk.Label(self.frame, text="Role")
        self.role_label.grid(row=2, column=0, padx=5, pady=5)
        self.role_combobox = ttk.Combobox(self.frame, values=["admin", "HR", "manager", "employee"])
        self.role_combobox.grid(row=2, column=1, padx=5, pady=5)

        self.create_button = tk.Button(self.frame, text="Create User", command=self.create_user)
        self.create_button.grid(row=3, column=0, padx=5, pady=5)

        self.update_button = tk.Button(self.frame, text="Update User", command=self.update_user)
        self.update_button.grid(row=3, column=1, padx=5, pady=5)

        self.delete_button = tk.Button(self.frame, text="Delete User", command=self.delete_user)
        self.delete_button.grid(row=3, column=2, padx=5, pady=5)

        self.tree = ttk.Treeview(self.frame, columns=("User ID", "Username", "Role"), show='headings')
        self.tree.heading("User ID", text="User ID")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Role", text="Role")
        self.tree.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
        self.load_users()

        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Program interrupted by user")
            self.cleanup()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(50) NOT NULL
            )
        """)
        self.conn.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_combobox.get()
        if not username or not password or not role:
            messagebox.showerror("Error", "All fields are required.")
            return
        try:
            hashed_password = self.hash_password(password)
            self.cursor.execute("""
                INSERT INTO users (username, password, role)
                VALUES (%s, %s, %s)
            """, (username, hashed_password, role))
            self.conn.commit()
            messagebox.showinfo("Success", "User created successfully.")
            self.load_users()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error creating user: {err}")

    def update_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No user selected.")
            return
        user_id = self.tree.item(selected_item)["values"][0]
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_combobox.get()
        if not username or not role:
            messagebox.showerror("Error", "Username and role are required.")
            return
        try:
            if password:
                hashed_password = self.hash_password(password)
                self.cursor.execute("""
                    UPDATE users SET username = %s, password = %s, role = %s
                    WHERE user_id = %s
                """, (username, hashed_password, role, user_id))
            else:
                self.cursor.execute("""
                    UPDATE users SET username = %s, role = %s
                    WHERE user_id = %s
                """, (username, role, user_id))
            self.conn.commit()
            messagebox.showinfo("Success", "User updated successfully.")
            self.load_users()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error updating user: {err}")

    def delete_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No user selected.")
            return
        user_id = self.tree.item(selected_item)["values"][0]
        try:
            self.cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "User deleted successfully.")
            self.load_users()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error deleting user: {err}")

    def load_users(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.cursor.execute("SELECT user_id, username, role FROM users")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def cleanup(self):
        self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    UserManagement()
