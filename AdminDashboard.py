import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from DatabaseConnection import create_connection


class AdminDashboard:
    def __init__(self, master):
        self.master = master
        self.master.title("EZRide - Admin Dashboard")
        self.master.geometry("1000x700")
        self.master.configure(bg="white")

        # Create Notebook (Tabbed UI)
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Add Tabs
        self.create_dashboard_tab()
        self.create_assign_booking_tab()
        self.create_view_bookings_tab()
        self.create_view_customers_tab()
        self.create_view_drivers_tab()
        self.create_generate_report_tab()  # New tab for generating reports

    def create_dashboard_tab(self):
        """Create the Dashboard Tab."""
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_tab, text="Dashboard")

        # Welcome Label
        welcome_label = tk.Label(self.dashboard_tab, text="Welcome, Admin!", font=("Arial", 28, "bold"), bg="white")
        welcome_label.pack(pady=30)

        # Logout Button
        logout_button = tk.Button(
            self.dashboard_tab,
            text="Logout",
            font=("Arial", 12),
            command=self.logout,
            bg="lightcoral",
            fg="white",
            width=15,
        )
        logout_button.pack(pady=20)

    def create_assign_booking_tab(self):
        """Create the Assign Booking Tab."""
        self.assign_booking_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.assign_booking_tab, text="Assign Booking")

        # Assign Driver Section
        tk.Label(self.assign_booking_tab, text="Assign Driver to Booking", font=("Arial", 20, "bold")).pack(pady=20)

        # Booking ID Input
        tk.Label(self.assign_booking_tab, text="Booking ID:", font=("Arial", 12)).pack(pady=5)
        self.booking_id_entry = tk.Entry(self.assign_booking_tab, font=("Arial", 12), width=40)
        self.booking_id_entry.pack(pady=5)

        # Driver ID Input
        tk.Label(self.assign_booking_tab, text="Driver ID:", font=("Arial", 12)).pack(pady=5)
        self.driver_id_entry = tk.Entry(self.assign_booking_tab, font=("Arial", 12), width=40)
        self.driver_id_entry.pack(pady=5)

        # Assign Button
        assign_button = tk.Button(
            self.assign_booking_tab,
            text="Assign Driver",
            font=("Arial", 12),
            command=self.assign_driver,
            bg="lightgreen",
            width=20,
        )
        assign_button.pack(pady=20)

    def create_view_bookings_tab(self):
        """Create the View Bookings Tab."""
        self.view_bookings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.view_bookings_tab, text="View Bookings")

        tk.Label(self.view_bookings_tab, text="All Bookings", font=("Arial", 20, "bold")).pack(pady=20)
        self.display_table("Bookings", self.view_bookings_tab, ["Booking ID", "Customer ID", "Pickup", "Dropoff", "Date", "Time", "Driver ID"])

    def create_view_customers_tab(self):
        """Create the View Customers Tab."""
        self.view_customers_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.view_customers_tab, text="View Customers")

        tk.Label(self.view_customers_tab, text="All Customers", font=("Arial", 20, "bold")).pack(pady=20)
        self.display_table("Customers", self.view_customers_tab, ["Customer ID", "Name", "Address", "Phone", "Email"])

    def create_view_drivers_tab(self):
        """Create the View Drivers Tab."""
        self.view_drivers_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.view_drivers_tab, text="View Drivers")

        tk.Label(self.view_drivers_tab, text="All Drivers", font=("Arial", 20, "bold")).pack(pady=20)
        self.display_table("Drivers", self.view_drivers_tab, ["Driver ID", "Name", "Phone", "Availability"])

    def create_generate_report_tab(self):
        """Create the Generate Report Tab."""
        self.generate_report_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.generate_report_tab, text="Generate Report")

        tk.Label(self.generate_report_tab, text="Generate Reports", font=("Arial",  20, "bold")).pack(pady=20)

        # Customer Report Button
        customer_report_button = tk.Button(
            self.generate_report_tab,
            text="Generate Customer Report",
            font=("Arial", 12),
            command=self.generate_customer_report,
            bg="lightblue",
            width=30,
        )
        customer_report_button.pack(pady=10)

        # Driver Report Button
        driver_report_button = tk.Button(
            self.generate_report_tab,
            text="Generate Driver Report",
            font=("Arial", 12),
            command=self.generate_driver_report,
            bg="lightblue",
            width=30,
        )
        driver_report_button.pack(pady=10)

        # Booking Report Button
        booking_report_button = tk.Button(
            self.generate_report_tab,
            text="Generate Booking Report",
            font=("Arial", 12),
            command=self.generate_booking_report,
            bg="lightblue",
            width=30,
        )
        booking_report_button.pack(pady=10)

        # Download All Reports Button
        download_all_button = tk.Button(
            self.generate_report_tab,
            text="Download All Reports",
            font=("Arial", 12),
            command=self.download_all_reports,
            bg="lightgreen",
            width=30,
        )
        download_all_button.pack(pady=20)

    def generate_customer_report(self):
        """Generate and save customer report."""
        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Customers")
            records = cursor.fetchall()

            report_content = "Customer ID, Name, Address, Phone, Email\n"
            for record in records:
                report_content += f"{record[0]}, {record[1]}, {record[2]}, {record[3]}, {record[4]}\n"

            self.save_report_to_file("Customer_Report.txt", report_content)
            messagebox.showinfo("Success", "Customer report generated successfully!")

        except Exception as e:
            messagebox.showerror("Database Error", f"Error generating customer report: {e}")
        finally:
            connection.close()

    def generate_driver_report(self):
        """Generate and save driver report."""
        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Drivers")
            records = cursor.fetchall()

            report_content = "Driver ID, Name, Phone, Availability\n"
            for record in records:
                report_content += f"{record[0]}, {record[1]}, {record[2]}, {record[3]}\n"

            self.save_report_to_file("Driver_Report.txt", report_content)
            messagebox.showinfo("Success", "Driver report generated successfully!")

        except Exception as e:
            messagebox.showerror("Database Error", f"Error generating driver report: {e}")
        finally:
            connection.close()

    def generate_booking_report(self):
        """Generate and save booking report."""
        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Bookings")
            records = cursor.fetchall()

            report_content = "Booking ID, Customer ID, Pickup, Dropoff, Date, Time, Driver ID\n"
            for record in records:
                report_content += f"{record[0]}, {record[1]}, {record[2]}, {record[3]}, {record[4]}, {record[5]}, {record[6]}\n"

            self.save_report_to_file("Booking_Report.txt", report_content)
            messagebox.showinfo("Success", "Booking report generated successfully!")

        except Exception as e:
            messagebox.showerror("Database Error", f"Error generating booking report: {e}")
        finally:
            connection.close()

    def save_report_to_file(self, filename, content):
        """Save report content to a file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=filename,
                                                   filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(content)

    def download_all_reports(self):
        """Download all reports."""
        self.generate_customer_report()
        self.generate_driver_report()
        self.generate_booking_report()

    def display_table(self, table_name, parent_frame, columns):
        """
        Generic function to fetch data from a table and display it in a Treeview table.
        """
        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            records = cursor.fetchall()

            # Create Treeview Widget
            tree = ttk.Treeview(parent_frame, columns=columns, show="headings", height=20)
            tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            # Add Headings
            for col in columns:
                tree.heading(col, text=col, anchor="center")
                tree.column(col, anchor="center", width=150)

            # Insert Data
            for record in records:
                tree.insert("", "end", values=record)

            # Add Delete and Update Buttons to Each Row
            tree.bind("<ButtonRelease-1>", lambda event, treeview=tree: self.on_row_click(event, treeview, table_name))

            # Add Scrollbars
            scrollbar_y = ttk.Scrollbar(parent_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar_y.set)
            scrollbar_y.pack(side="right", fill="y")

        except Exception as e:
            messagebox.showerror("Database Error", f"Error fetching {table_name} data: {e}")
        finally:
            connection.close()

    def on_row_click(self, event, treeview, table_name):
        """Handle row click to show delete and update options."""
        item = treeview.selection()[0]
        values = treeview.item(item)["values"]

        if table_name == "Customers":
            self.show_customer_options(values, treeview, item)
        elif table_name == "Drivers":
            self.show_driver_options(values, treeview, item)

    def show_customer_options(self, values, treeview, item):
        """Show options for deleting/updating a customer."""
        customer_id = values[0]
        action = messagebox.askquestion("Customer Options", f"Do you want to update or delete this customer?\nID: {customer_id}")

        if action == "yes":
            # Handle Update or Delete (Assuming a simple pop-up for Update)
            self.update_customer(customer_id, treeview, item)

    def show_driver_options(self, values, treeview, item):
        """Show options for deleting/updating a driver."""
        driver_id = values[0]
        action = messagebox.askquestion("Driver Options", f"Do you want to update or delete this driver?\nID: {driver_id}")

        if action == "yes":
            # Handle Update or Delete (Assuming a simple pop-up for Update)
            self.update_driver(driver_id, treeview, item)

    def update_customer(self, customer_id, treeview, item):
        """Update customer details."""
        # For simplicity, assuming the update form is a small pop-up with entry fields
        def save_changes():
            name = name_entry.get()
            address = address_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()

            if not name or not address or not phone or not email:
                messagebox.showerror("Input Error", "All fields must be filled!")
                return

            try:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE Customers SET name = %s, address = %s, phone = %s, email = %s WHERE customer_id = %s
                """, (name, address, phone, email, customer_id))
                connection.commit()
                treeview.item(item, values=(customer_id, name, address, phone, email))
                messagebox.showinfo("Success", "Customer updated successfully!")
            except Exception as e:
                messagebox.showerror("Database Error", f"Error updating customer: {e}")
            finally:
                connection.close()
                update_window.destroy()

        update_window = tk.Toplevel(self.master)
        update_window.title(f"Update Customer - {customer_id}")

        tk.Label(update_window, text="Name:").grid(row=0, column=0)
        tk.Label(update_window, text="Address:").grid(row=1, column=0)
        tk.Label(update_window, text="Phone:").grid(row=2, column=0)
        tk.Label(update_window, text="Email:").grid(row=3, column=0)

        name_entry = tk.Entry(update_window)
        address_entry = tk.Entry(update_window)
        phone_entry = tk.Entry(update_window)
        email_entry = tk.Entry(update_window)

        name_entry.grid(row=0, column=1)
        address_entry.grid(row=1, column=1)
        phone_entry.grid(row=2, column=1)
        email_entry.grid(row=3, column=1)

        save_button = tk.Button(update_window, text="Save Changes", command=save_changes)
        save_button.grid(row=4, columnspan=2)

        update_window.mainloop()

    def update_driver(self, driver_id, treeview, item):
        """Update driver details."""
        def save_changes():
            name = name_entry.get()
            phone = phone_entry.get()
            availability = availability_entry.get()

            if not name or not phone or not availability:
                messagebox.showerror("Input Error ", "All fields must be filled!")
                return

            try:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE Drivers SET name = %s, phone = %s, availability = %s WHERE driver_id = %s
                """, (name, phone, availability, driver_id))
                connection.commit()
                treeview.item(item, values=(driver_id, name, phone, availability))
                messagebox.showinfo("Success", "Driver updated successfully!")
            except Exception as e:
                messagebox.showerror("Database Error", f"Error updating driver: {e}")
            finally:
                connection.close()
                update_window.destroy()

        update_window = tk.Toplevel(self.master)
        update_window.title(f"Update Driver - {driver_id}")

        tk.Label(update_window, text="Name:").grid(row=0, column=0)
        tk.Label(update_window, text="Phone:").grid(row=1, column=0)
        tk.Label(update_window, text="Availability:").grid(row=2, column=0)

        name_entry = tk.Entry(update_window)
        phone_entry = tk.Entry(update_window)
        availability_entry = tk.Entry(update_window)

        name_entry.grid(row=0, column=1)
        phone_entry.grid(row=1, column=1)
        availability_entry.grid(row=2, column=1)

        save_button = tk.Button(update_window, text="Save Changes", command=save_changes)
        save_button.grid(row=3, columnspan=2)

        update_window.mainloop()

    def delete_customer(self, customer_id, treeview, item):
        """Delete a customer."""
        confirmation = messagebox.askyesno("Delete Customer", f"Are you sure you want to delete customer {customer_id}?")
        if confirmation:
            try:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute("DELETE FROM Customers WHERE customer_id = %s", (customer_id,))
                connection.commit()
                treeview.delete(item)
                messagebox.showinfo("Success", "Customer deleted successfully!")
            except Exception as e:
                messagebox.showerror("Database Error", f"Error deleting customer: {e}")
            finally:
                connection.close()

    def delete_driver(self, driver_id, treeview, item):
        """Delete a driver."""
        confirmation = messagebox.askyesno("Delete Driver", f"Are you sure you want to delete driver {driver_id}?")
        if confirmation:
            try:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute("DELETE FROM Drivers WHERE driver_id = %s", (driver_id,))
                connection.commit()
                treeview.delete(item)
                messagebox.showinfo("Success", "Driver deleted successfully!")
            except Exception as e:
                messagebox.showerror("Database Error", f"Error deleting driver: {e}")
            finally:
                connection.close()

    def assign_driver(self):
        """Assign a driver to a booking."""
        booking_id = self.booking_id_entry.get()
        driver_id = self.driver_id_entry.get()

        if not booking_id or not driver_id:
            messagebox.showerror("Input Error", "Both Booking ID and Driver ID are required!")
            return

        try:
            connection = create_connection()
            cursor = connection.cursor()

            # Check if driver is already booked
            cursor.execute("""
                SELECT booking_date, booking_time FROM Bookings WHERE driver_id = %s
            """, (driver_id,))
            existing_bookings = cursor.fetchall()

            booking_date = "2024-08-01"  # Example for simplicity
            booking_time = "10:00 AM"

            for existing_booking in existing_bookings:
                if existing_booking[0] == booking_date and existing_booking[1] == booking_time:
                    messagebox.showerror("Driver Unavailable", "The driver is already booked for this time.")
                    return

            # Assign Driver
            cursor.execute("""
                UPDATE Bookings
                SET driver_id = %s
                WHERE booking_id = %s
            """, (driver_id, booking_id))

            connection.commit()
            messagebox.showinfo("Success", "Driver assigned successfully!")

        except Exception as e:
            messagebox.showerror("Database Error", f"Error: {e}")
        finally:
            connection.close()

    def logout(self):
        """Logs out the admin."""
        self.master.quit()


# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()