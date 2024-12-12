import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from Dashboard import Dashboard
from DatabaseConnection import create_connection

class AdminDashboard(Dashboard):
    def _init_(self, master):
        self.master = master
        self.master.title("EZRide - Admin Dashboard")
        self.master.geometry("1000x700")
        self.master.configure(bg="white")

        # Create main frame for better organization
        self.main_frame = tk.Frame(self.master, bg="white")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Logo / Branding
        self.logo_label = tk.Label(self.main_frame, text="EZRide", font=("Arial", 24, "bold"), fg="green", bg="white")
        self.logo_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Driver Assignment Section
        self.driver_assignment_frame = tk.Frame(self.main_frame, bg="white")
        self.driver_assignment_frame.grid(row=1, column=0, pady=20, padx=20, sticky="w")

        # Assign Driver to Booking
        self.booking_id_label = tk.Label(self.driver_assignment_frame, text="Booking ID", font=("Arial", 12), bg="white")
        self.booking_id_label.grid(row=0, column=0, pady=5, sticky="w")

        self.booking_id_entry = tk.Entry(self.driver_assignment_frame, font=("Arial", 12), width=40)
        self.booking_id_entry.grid(row=0, column=1, pady=5)

        self.driver_id_label = tk.Label(self.driver_assignment_frame, text="Driver ID", font=("Arial", 12), bg="white")
        self.driver_id_label.grid(row=1, column=0, pady=5, sticky="w")

        self.driver_id_entry = tk.Entry(self.driver_assignment_frame, font=("Arial", 12), width=40)
        self.driver_id_entry.grid(row=1, column=1, pady=5)

        self.assign_button = tk.Button(self.driver_assignment_frame, text="Assign Driver", font=("Arial", 12), command=self.assign_driver, bg="lightgreen", width=20)
        self.assign_button.grid(row=2, column=0, pady=10)

        # View Records Section
        self.view_records_frame = tk.Frame(self.main_frame, bg="white")
        self.view_records_frame.grid(row=2, column=0, pady=20, padx=20)

        self.view_bookings_button = tk.Button(self.view_records_frame, text="View All Bookings", font=("Arial", 12), command=self.view_bookings, bg="lightyellow", width=20)
        self.view_bookings_button.grid(row=0, column=0, pady=10)

        self.view_customers_button = tk.Button(self.view_records_frame, text="View All Customers", font=("Arial", 12), command=self.view_customers, bg="lightyellow", width=20)
        self.view_customers_button.grid(row=1, column=0, pady=10)

        self.view_drivers_button = tk.Button(self.view_records_frame, text="View All Drivers", font=("Arial", 12), command=self.view_drivers, bg="lightyellow", width=20)
        self.view_drivers_button.grid(row=2, column=0, pady=10)

        # Logout Button
        self.logout_button = tk.Button(self.main_frame, text="Logout", font=("Arial", 12), command=self.logout, bg="lightcoral", width=20)
        self.logout_button.grid(row=3, column=0, pady=20, padx=20)

    def assign_driver(self):
        """
        Assign a driver to a booking after checking for overlaps.
        """
        booking_id = self.booking_id_entry.get()
        driver_id = self.driver_id_entry.get()

        if not booking_id or not driver_id:
            messagebox.showerror("Input Error", "Both Booking ID and Driver ID are required!")
            return

        # Check if the driver is available at the specified booking time
        try:
            connection = create_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT booking_date, booking_time FROM Bookings WHERE driver_id = %s
            """, (driver_id,))
            existing_bookings = cursor.fetchall()

            booking_date = simpledialog.askstring("Booking Date", "Enter the booking date (YYYY-MM-DD):")
            booking_time = simpledialog.askstring("Booking Time", "Enter the booking time (HH:MM):")

            for existing_booking in existing_bookings:
                if existing_booking[0] == booking_date and existing_booking[1] == booking_time:
                    messagebox.showerror("Driver Unavailable", "The driver is already booked for this time.")
                    return

            # Assign the driver to the booking
            cursor.execute("""
                UPDATE Bookings
                SET driver_id = %s
                WHERE booking_id = %s
            """, (driver_id, booking_id))

            connection.commit()
            messagebox.showinfo("Driver Assigned", "Driver has been successfully assigned to the booking!")
        except Exception as e:
            messagebox.showerror("Database Error", f"Error assigning driver: {e}")
        finally:
            connection.close()

    def view_bookings(self):

        try:
            connection = create_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM Bookings")
            bookings = cursor.fetchall()

            self.show_records("Bookings", ["Booking ID", "Customer ID", "Pickup Location", "Dropoff Location", "Booking Date", "Booking Time", "Driver ID"], bookings)
        except Exception as e:
            messagebox.showerror("Database Error", f"Error fetching bookings: {e}")
        finally:
            connection.close()

    def view_customers(self):

        try:
            connection = create_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM Customers")
            customers = cursor.fetchall()

            self.show_records("Customers", ["Customer ID", "Name", "Address", "Phone Number", "Email"], customers)
        except Exception as e:
            messagebox.showerror("Database Error", f"Error fetching customers: {e}")
        finally:
            connection.close()

    def view_drivers(self):
        """
        Fetch and display all drivers.
        """
        try:
            connection = create_connection()
            cursor = connection.cursor()

            # Fetch only the necessary columns (correct column names)
            cursor.execute("SELECT driver_id, name, phone_number, availability_status FROM Drivers")
            drivers = cursor.fetchall()

            self.show_records("Drivers", ["Driver ID", "Name", "Phone Number", "Availability"], drivers)
        except Exception as e:
            messagebox.showerror("Database Error", f"Error fetching drivers: {e}")
        finally:
            connection.close()

    def show_records(self, record_type, columns, records):
        """
        Display records in a new window.
        """
        records_window = tk.Toplevel(self.master)
        records_window.title(f"View All {record_type}")
        records_window.geometry("800x600")

        tree = ttk.Treeview(records_window, columns=columns, show="headings")
        tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            tree.heading(col, text=col)

        for record in records:
            tree.insert("", "end", values=record)

    def logout(self):
        """
        Logs out and closes the application.
        """
        self.master.quit()

# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    admin_dashboard = AdminDashboard(root)
    root.mainloop()