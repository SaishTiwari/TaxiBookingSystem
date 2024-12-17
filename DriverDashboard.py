import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import webbrowser
from DatabaseConnection import create_connection  # Ensure you have a database connection module


class DriverDashboard:
    def __init__(self, master, user_id):
        self.master = master
        self.user_id = user_id
        self.master.title("Driver Dashboard")
        self.master.geometry("800x600")
        self.master.configure(bg="white")

        # Create Notebook for Tabs
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create Tabs
        self.create_pending_requests_tab()
        self.create_ride_history_tab()

        # Logout Button
        self.logout_button = tk.Button(self.master, text="Logout", command=self.logout, bg="#ff4d4d", fg="white", font=("Arial", 12))
        self.logout_button.pack(pady=10)

    def create_pending_requests_tab(self):
        self.pending_requests_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.pending_requests_tab, text="Pending Requests")

        # Title Label
        title_label = tk.Label(self.pending_requests_tab, text="Pending Ride Requests", font=("Arial", 20, "bold"), bg="white")
        title_label.pack(pady=20)

        # Treeview for Ride Requests
        self.treeview = ttk.Treeview(self.pending_requests_tab,
                                     columns=("Booking ID", "Customer Name", "Pickup Location", "Dropoff Location"),
                                     show="headings")
        self.treeview.heading("Booking ID", text="Booking ID")
        self.treeview.heading("Customer Name", text="Customer Name")
        self.treeview.heading("Pickup Location", text="Pickup Location")
        self.treeview.heading("Dropoff Location", text="Dropoff Location")
        self.treeview.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Load Pending Ride Requests
        self.load_pending_requests()

        # Accept and Decline Buttons
        button_frame = tk.Frame(self.pending_requests_tab, bg="white")
        button_frame.pack(pady=10)

        self.accept_button = tk.Button(button_frame, text="Accept", command=self.accept_selected_ride, bg="#4CAF50", fg="white")
        self.accept_button.pack(side=tk.LEFT, padx=5)

        self.decline_button = tk.Button(button_frame, text="Decline", command=self.decline_selected_ride, bg="#ff4d4d", fg="white")
        self.decline_button.pack(side=tk.LEFT, padx=5)

    def load_pending_requests(self):
        """Fetch and display pending ride requests."""
        # Clear the treeview before loading new data
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        connection = create_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT b.booking_id, c.name, b.pickup_location, b.dropoff_location
                FROM Bookings b
                JOIN Customers c ON b.customer_id = c.customer_id
                WHERE b.driver_id IS NULL AND b.status = 'Pending'
            """)

            bookings = cursor.fetchall()

            for booking in bookings:
                booking_id, customer_name, pickup_location, dropoff_location = booking
                self.treeview.insert("", "end", values=(booking_id, customer_name, pickup_location, dropoff_location))

        except Exception as e:
            messagebox.showerror("Database Error", f"Error loading ride requests: {e}")
        finally:
            connection.close()

    def accept_selected_ride(self):
        """Accept the selected ride."""
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a ride request to accept.")
            return

        booking_id = self.treeview.item(selected_item, "values")[0]
        self.accept_ride(booking_id)

    def decline_selected_ride(self):
        """Decline the selected ride."""
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a ride request to decline.")
            return

        booking_id = self.treeview.item(selected_item, "values")[0]
        self.decline_ride(booking_id)

    def accept_ride(self, booking_id):
        """Accept the ride and update the booking status."""
        connection = create_connection()
        cursor = connection.cursor()

        try:
            # Update the booking
            cursor.execute("""
                UPDATE Bookings
                SET driver_id = %s, status = 'Accepted'
                WHERE booking_id = %s
 """, (self.user_id, booking_id))

            # Update the driver availability
            cursor.execute("""
                UPDATE Drivers
                SET availability_status = 'Not Available'
                WHERE driver_id = %s
            """, (self.user_id,))

            connection.commit()
            messagebox.showinfo("Success", "You have accepted the ride!")
            self.load_pending_requests()

            # Fetch the pickup and dropoff locations
            cursor.execute("""
                SELECT pickup_location, dropoff_location FROM Bookings WHERE booking_id = %s
            """, (booking_id,))
            pickup, dropoff = cursor.fetchone()

            self.show_map(pickup, dropoff)

        except Exception as e:
            messagebox.showerror("Database Error", f"Error accepting the ride: {e}")
        finally:
            connection.close()

    def decline_ride(self, booking_id):
        """Decline the ride request."""
        connection = create_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                UPDATE Bookings
                SET status = 'Declined'
                WHERE booking_id = %s
            """, (booking_id,))
            connection.commit()
            messagebox.showinfo("Success", "You have declined the ride!")
            self.load_pending_requests()

        except Exception as e:
            messagebox.showerror("Database Error", f"Error declining the ride: {e}")
        finally:
            connection.close()

    def create_ride_history_tab(self):
        self.ride_history_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.ride_history_tab, text="Ride History")

        # Title Label
        title_label = tk.Label(self.ride_history_tab, text="Your Ride History", font=("Arial", 20, "bold"), bg="white")
        title_label.pack(pady=20)

        # Treeview for Ride History
        self.history_treeview = ttk.Treeview(self.ride_history_tab,
                                              columns=("Booking ID", "Customer Name", "Pickup Location", "Dropoff Location", "Status"),
                                              show="headings")
        self.history_treeview.heading("Booking ID", text="Booking ID")
        self.history_treeview.heading("Customer Name", text="Customer Name")
        self.history_treeview.heading("Pickup Location", text="Pickup Location")
        self.history_treeview.heading("Dropoff Location", text="Dropoff Location")
        self.history_treeview.heading("Status", text="Status")
        self.history_treeview.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.load_ride_history()

    def load_ride_history(self):
        connection = create_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                SELECT b.booking_id, c.name, b.pickup_location, b.dropoff_location, b.status
                FROM Bookings b
                JOIN Customers c ON b.customer_id = c.customer_id
                WHERE b.driver_id = %s
            """, (self.user_id,))

            history = cursor.fetchall()

            for record in history:
                self.history_treeview.insert("", "end", values=record)

        except Exception as e:
            messagebox.showerror("Database Error", f"Error loading ride history: {e}")
        finally:
            connection.close()

    def show_map(self, pickup_location, dropoff_location):
        """Open Google Maps with the route from pickup to dropoff location."""
        pickup_location = pickup_location.replace(" ", "+")
        dropoff_location = dropoff_location.replace(" ", "+")
        google_maps_url = f"https://www.google.com/maps/dir/?api=1&origin={pickup_location}&destination={dropoff_location}&travelmode=driving"
        webbrowser.open(google_maps_url)

    def logout(self):
        """Handle logout action."""
        self.master.destroy()  # Close the application or redirect to login screen

# To run the dashboard
if __name__ == "__main__":
    root = tk.Tk()
    driver_dashboard = DriverDashboard(root, 1)
    root.mainloop()