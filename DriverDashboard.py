import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import webbrowser

from Dashboard import Dashboard
from DatabaseConnection import create_connection  # Ensure you have a database connection module


class DriverDashboard(Dashboard):
    def _init_(self, master, driver_id):
        self.master = master
        self.master.title("Driver Dashboard")
        self.master.geometry("800x600")
        self.master.configure(bg="white")
        self.driver_id = driver_id

        self.main_frame = tk.Frame(self.master, bg="white")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title Label
        self.title_label = tk.Label(self.main_frame, text="Pending Ride Requests", font=("Arial", 20, "bold"),
                                    bg="white")
        self.title_label.pack(pady=20)

        # Ride Requests List (Treeview)
        self.treeview = ttk.Treeview(self.main_frame,
                                     columns=("Booking ID", "Customer Name", "Pickup Location", "Dropoff Location"),
                                     show="headings")
        self.treeview.heading("Booking ID", text="Booking ID")
        self.treeview.heading("Customer Name", text="Customer Name")
        self.treeview.heading("Pickup Location", text="Pickup Location")
        self.treeview.heading("Dropoff Location", text="Dropoff Location")
        self.treeview.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Accept and Decline Buttons for each request
        self.load_pending_requests()

    def load_pending_requests(self):

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
                # Add Accept and Decline buttons for each row
                self.add_buttons_for_ride(booking_id)

        except Exception as e:
            messagebox.showerror("Database Error", f"Error loading ride requests: {e}")
        finally:
            connection.close()

    def add_buttons_for_ride(self, booking_id):
        """
        Add Accept and Decline buttons for each ride request.
        """
        accept_button = tk.Button(self.main_frame, text="Accept", command=lambda: self.accept_ride(booking_id))
        accept_button.pack(pady=5, side=tk.LEFT)

        decline_button = tk.Button(self.main_frame, text="Decline", command=lambda: self.decline_ride(booking_id))
        decline_button.pack(pady=5, side=tk.LEFT)

    def accept_ride(self, booking_id):
        """
        Accept the ride and update driver availability status.
        """
        connection = create_connection()
        cursor = connection.cursor()

        try:
            # Accept the booking
            cursor.execute("""
                UPDATE Bookings
                SET driver_id = %s, status = 'Accepted'
                WHERE booking_id = %s
            """, (self.driver_id, booking_id))

            # Update driver availability status
            cursor.execute("""
                UPDATE Drivers
                SET availability_status = 'Not Available'
                WHERE driver_id = %s
            """, (self.driver_id,))

            connection.commit()
            messagebox.showinfo("Success", "You have accepted the ride!")
            self.load_pending_requests()  # Reload the ride requests to reflect changes

            # Fetch the pickup and dropoff locations
            cursor.execute("""
                SELECT pickup_location, dropoff_location FROM Bookings WHERE booking_id = %s
            """, (booking_id,))
            pickup, dropoff = cursor.fetchone()

            self.show_map(pickup, dropoff)  # Show the map for the accepted ride

        except Exception as e:
            messagebox.showerror("Database Error", f"Error accepting the ride: {e}")
        finally:
            connection.close()

    def decline_ride(self, booking_id):
        """
        Decline the ride request.
        """
        connection = create_connection()
        cursor = connection.cursor()

        try:
            # Update status to 'Declined'
            cursor.execute("""
                UPDATE Bookings
                SET status = 'Declined'
                WHERE booking_id = %s
            """, (booking_id,))

            connection.commit()
            messagebox.showinfo("Success", "You have declined the ride!")
            self.load_pending_requests()  # Reload the ride requests to reflect changes

        except Exception as e:
            messagebox.showerror("Database Error", f"Error declining the ride: {e}")
        finally:
            connection.close()

    def show_map(self, pickup_location, dropoff_location):
        """
        Open Google Maps in a web browser showing the route from pickup to dropoff location.
        """
        # Replace spaces with '+' for URL encoding
        pickup_location = pickup_location.replace(" ", "+")
        dropoff_location = dropoff_location.replace(" ", "+")

        # Google Maps URL with directions
        google_maps_url = f"https://www.google.com/maps/dir/?api=1&origin={pickup_location}&destination={dropoff_location}&travelmode=driving"

        # Open the URL in a web browser
        webbrowser.open(google_maps_url)


# To run the dashboard
if __name__ == "__main__":
    root = tk.Tk()
    driver_id = 1  # Example driver ID (this will be dynamic in a real application)
    driver_dashboard = DriverDashboard(root, driver_id)
    root.mainloop()