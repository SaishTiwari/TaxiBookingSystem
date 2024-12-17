import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
import mysql.connector

from Dashboard import Dashboard


def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="pcps@123",
        database="taxibookingsystem"
    )


class CustomerDashboard(Dashboard):
    def __init__(self, master, user_id):
        super().__init__(master, user_id)
        self.root = root
        self.root.title("Taxi Booking System")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.create_booking_tab()
        self.create_view_bookings_tab()

        logout_button = tk.Button(self.root, text="Logout", command=self.logout, bg="#ff4d4d", fg="white", font=("Arial", 12), width=20)
        logout_button.pack(pady=10)

    def create_booking_tab(self):
        self.booking_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.booking_tab, text="Book a Ride")

        title_label = tk.Label(self.booking_tab, text="Book Your Taxi", font=("Arial", 18, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)

        tk.Label(self.booking_tab, text="Pickup Location:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        self.pickup_entry = tk.Entry(self.booking_tab, width=40, font=("Arial", 12))
        self.pickup_entry.pack(pady=5)

        tk.Label(self.booking_tab, text="Drop-off Location:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        self.dropoff_entry = tk.Entry(self.booking_tab, width=40, font=("Arial", 12))
        self.dropoff_entry.pack(pady=5)

        tk.Label(self.booking_tab, text="Booking Date:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        self.calendar = Calendar(self.booking_tab, selectmode="day", mindate=datetime.today())
        self.calendar.pack(pady=5)

        tk.Label(self.booking_tab, text="Booking Time:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        time_frame = tk.Frame(self.booking_tab, bg="#f0f0f0")
        time_frame.pack(pady=5)

        self.time_hour = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(24)], width=5, font=("Arial", 12))
        self.time_hour.set("00")
        self.time_hour.pack(side=tk.LEFT, padx=5)

        tk.Label(time_frame, text=":", font=("Arial", 12), bg="#f0f0f0").pack(side=tk.LEFT)

        self.time_minute = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(60)], width=5, font=("Arial", 12))
        self.time_minute.set("00")
        self.time_minute.pack(side=tk.LEFT, padx=5)

        book_button = tk.Button(self.booking_tab, text="Book Taxi", command=self.book_taxi, bg="#4CAF50", fg="white", font=("Arial", 12), width=20)
        book_button.pack(pady=20)

    def create_view_bookings_tab(self):
        self.view_bookings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.view_bookings_tab, text="View Bookings")

        title_label = tk.Label(self.view_bookings_tab, text="Your Booking History", font=("Arial", 18, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)

        self.tree = ttk.Treeview(self.view_bookings_tab, columns=("Booking ID", "Pickup", "Dropoff", "Date", "Time"), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.tree.heading("Booking ID", text="Booking ID")
        self.tree.heading("Pickup", text="Pickup Location")
        self.tree.heading("Dropoff", text="Dropoff Location")
        self.tree.heading("Date", text="Booking Date")
        self.tree.heading("Time", text="Booking Time")

        self.tree.column("Booking ID", width=100)
        self.tree.column("Pickup", width =150)
        self.tree.column("Dropoff", width=150)
        self.tree.column("Date", width=100)
        self.tree.column("Time", width=100)

        self.load_bookings()

    def load_bookings(self):
        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Bookings WHERE customer_id = 1")  # Example for customer_id = 1
            bookings = cursor.fetchall()

            for booking in bookings:
                self.tree.insert("", tk.END, values=(booking[0], booking[2], booking[3], booking[4], booking[5]))
        except Exception as e:
            messagebox.showerror("Database Error", f"Error fetching bookings: {e}")
        finally:
            connection.close()

    def book_taxi(self):
        pickup_location = self.pickup_entry.get()
        dropoff_location = self.dropoff_entry.get()
        booking_date = self.calendar.get_date()
        booking_time = f"{self.time_hour.get()}:{self.time_minute.get()}"

        if not pickup_location or not dropoff_location or not booking_date or not booking_time:
            messagebox.showerror("Booking Error", "Please fill in all fields.")
            return

        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO Bookings (customer_id, pickup_location, dropoff_location, booking_date, booking_time)
                VALUES (%s, %s, %s, %s, %s)
            """, (1, pickup_location, dropoff_location, booking_date, booking_time))

            connection.commit()
            messagebox.showinfo("Booking Successful", "Your taxi has been booked successfully!")
            self.load_bookings()  # Refresh the booking history
        except Exception as e:
            messagebox.showerror("Database Error", f"Error during booking: {e}")
        finally:
            connection.close()

    def logout(self):
        self.root.quit()

    def runapp(self):
        self.master.main



if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerDashboard(root, 1)
    root.mainloop()