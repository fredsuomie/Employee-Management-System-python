import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

class PerformanceEvaluation:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='sip3.cjuo44okojjd.ap-south-1.rds.amazonaws.com',
            port=3306,
            user='root',
            password='BCAH5-2024',
            database='emp1'
        )
        self.cursor = self.conn.cursor()

    def record_performance_review(self, employee_id, criteria, rating, review, evaluation_date):
        self.cursor.execute("""
        INSERT INTO performance_evaluation (employee_id, criteria, rating, review, evaluation_date)
        VALUES (%s, %s, %s, %s, %s)
        """, (employee_id, criteria, rating, review, evaluation_date))
        self.conn.commit()
        messagebox.showinfo("Success", "Performance review recorded successfully")

    def get_performance_evaluations(self):
        self.cursor.execute("SELECT * FROM performance_evaluation")
        return self.cursor.fetchall()

class PerformanceEvaluationApp:
    def __init__(self, root, performance_evaluation):
        self.performance_evaluation = performance_evaluation

        self.root = root
        self.root.title("Performance Evaluation")

        #  background image
        self.background_image = Image.open("Background.jpeg")  # Ensure this image path is correct
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.background_label = Label(self.root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        # frame to hold the widgets
        self.frame = Frame(root, bg='white')
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=0.8, relheight=0.8)

        # Form fields
        self.employee_id_label = Label(self.frame, text="Employee ID", bg='white')
        self.employee_id_label.grid(row=0, column=0, pady=10, padx=10)
        self.employee_id_entry = Entry(self.frame)
        self.employee_id_entry.grid(row=0, column=1, pady=10, padx=10)

        self.criteria_label = Label(self.frame, text="Criteria", bg='white')
        self.criteria_label.grid(row=1, column=0, pady=10, padx=10)
        self.criteria_entry = Entry(self.frame)
        self.criteria_entry.grid(row=1, column=1, pady=10, padx=10)

        self.rating_label = Label(self.frame, text="Rating", bg='white')
        self.rating_label.grid(row=2, column=0, pady=10, padx=10)
        self.rating_entry = Entry(self.frame)
        self.rating_entry.grid(row=2, column=1, pady=10, padx=10)

        self.review_label = Label(self.frame, text="Review", bg='white')
        self.review_label.grid(row=3, column=0, pady=10, padx=10)
        self.review_entry = Entry(self.frame)
        self.review_entry.grid(row=3, column=1, pady=10, padx=10)

        self.evaluation_date_label = Label(self.frame, text="Evaluation Date (YYYY-MM-DD)", bg='white')
        self.evaluation_date_label.grid(row=4, column=0, pady=10, padx=10)
        self.evaluation_date_entry = Entry(self.frame)
        self.evaluation_date_entry.grid(row=4, column=1, pady=10, padx=10)

        self.record_button = Button(self.frame, text="Record Performance Review", command=self.record_performance_review, bg='lightblue')
        self.record_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Data table for performance evaluations
        self.tree = ttk.Treeview(root, columns=("evaluation_id", "employee_id", "criteria", "rating", "review", "evaluation_date"), show='headings')
        self.tree.heading("evaluation_id", text="Evaluation ID")
        self.tree.heading("employee_id", text="Employee ID")
        self.tree.heading("criteria", text="Criteria")
        self.tree.heading("rating", text="Rating")
        self.tree.heading("review", text="Review")
        self.tree.heading("evaluation_date", text="Evaluation Date")
        self.tree.place(relx=0.5, rely=0.8, anchor=CENTER, relwidth=0.8, relheight=0.4)

        self.refresh_performance_evaluations()

    def record_performance_review(self):
        employee_id = self.employee_id_entry.get()
        criteria = self.criteria_entry.get()
        rating = self.rating_entry.get()
        review = self.review_entry.get()
        evaluation_date = self.evaluation_date_entry.get()

        self.performance_evaluation.record_performance_review(employee_id, criteria, rating, review, evaluation_date)
        self.refresh_performance_evaluations()

    def refresh_performance_evaluations(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        performance_evaluations = self.performance_evaluation.get_performance_evaluations()
        for evaluation in performance_evaluations:
            self.tree.insert('', 'end', values=evaluation)

    def cleanup(self):
        self.performance_evaluation.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    performance_evaluation = PerformanceEvaluation()
    performance_evaluation_app = PerformanceEvaluationApp(root, performance_evaluation)
    root.protocol("WM_DELETE_WINDOW", performance_evaluation_app.cleanup)  # Ensure database connection is closed on exit
    root.mainloop()
