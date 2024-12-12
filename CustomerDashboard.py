import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
import requests
import mysql.connector

from Dashboard import Dashboard


def create_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="pcps@123",
        database="taxibookingsystem"
    )


def calculate_fare(pickup_location, dropoff_location):

    API_KEY = ""
    endpoint = "https://maps.googleapis.com/maps/api/distancematrix/json"

    params = {
        "origins": pickup_location,
        "destinations": dropoff_location,
        "units": "metric",
        "key": API_KEY
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()

        # Validate response structure
        if data["status"] != "OK" or "rows" not in data:
            raise ValueError("Invalid response from Google Maps API")

        # Extract distance in kilometers
        distance_info = data["rows"][0]["elements"][0]
        if distance_info["status"] != "OK":
            raise ValueError(f"Error in calculating distance: {distance_info['status']}")

        distance_km = distance_info["distance"]["value"] / 1000

        # Calculate fare
        base_fare = 50
        fare_per_km = 70
        total_fare = base_fare + (distance_km * fare_per_km)
        return round(total_fare, 2)

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API request failed: {e}")
    except (KeyError, IndexError, ValueError) as e:
        raise RuntimeError(f"Error processing API response: {e}")


class CustomerDashboard(Dashboard):
    def __init__(self, root):
        super().__init__(1)
        for widget in root.winfo_children():
            widget.destroy()
        self.root = root
        self.root.title("Taxi Booking System")
        self.root.geometry("400x500")

        # Pickup location
        tk.Label(root, text="Pickup Location:").pack(pady=5)
        self.pickup_entry = tk.Entry(root, width=40)
        self.pickup_entry.pack(pady=5)

        # Drop-off location
        tk.Label(root, text="Drop-off Location:").pack(pady=5)
        self.dropoff_entry = tk.Entry(root, width=40)
        self.dropoff_entry.pack(pady=5)

        # Booking date with limit
        today = datetime.today()
        tk.Label(root, text="Booking Date:").pack(pady=5)
        self.calendar = Calendar(root, selectmode="day", mindate=today)
        self.calendar.pack(pady=5)

        # Booking time
        tk.Label(root, text="Booking Time:").pack(pady=5)
        time_frame = tk.Frame(root)
        time_frame.pack(pady=5)


        self.time_hour = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(24)], width=5)
        self.time_hour.set("00")
        self.time_hour.pack(side=tk.LEFT, padx=5)

        tk.Label(time_frame, text=":").pack(side=tk.LEFT)

        self.time_minute = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(60)], width=5)
        self.time_minute.set("00")
        self.time_minute.pack(side=tk.LEFT, padx=5)

        # Submit button
        tk.Button(root, text="Book Taxi", command=self.book_taxi, bg="green", fg="black").pack(pady=20)

    def book_taxi(self):
        """
        Handles the booking of a taxi and calculates fare using Google Maps API.
        """
        pickup_location = self.pickup_entry.get()
        dropoff_location = self.dropoff_entry.get()
        booking_date = self.calendar.get_date()
        booking_time = f"{self.time_hour.get()}:{self.time_minute.get()}"



        try:
            # Calculate fare
            fare = calculate_fare(pickup_location, dropoff_location)

            # Ask customer to confirm the fare
            confirmation = messagebox.askyesno(
                "Confirm Fare",
                f"The calculated fare for your ride is ₹{fare:.2f}. Do you want to proceed with the booking?"
            )

            if not confirmation:
                messagebox.showinfo("Booking Cancelled", "Your booking was not completed.")
                return

            # Save booking to the database
            connection = create_connection()
            cursor = connection.cursor()

            # Assuming customer_id = 1 for simplicity
            cursor.execute("""
                INSERT INTO Bookings (customer_id, pickup_location, dropoff_location, booking_date, booking_time, fare)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (1, pickup_location, dropoff_location, booking_date, booking_time, fare))

            connection.commit()
            messagebox.showinfo("Booking Successful", "Your taxi has been booked successfully!")
        except RuntimeError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Database Error", f"Error during booking: {e}")
        finally:
            if 'connection' in globals():
                connection.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerDashboard(root)
    root.mainloop()

    # import tkinter as tk
    # from tkinter import messagebox, simpledialog
    # from tkcalendar import Calendar
    # from tkinter import ttk
    # import webbrowser
    # from DatabaseConnection import create_connection  # Assume this function handles DB connection
    # from path.Utils import remove_widgets
    #
    #
    # class CustomerDashboard:
    #     def __init__(self, master, customer_id):
    #
    #         remove_widgets(master)
    #
    #         self.master = master
    #
    #         self.master.title("EZRide - Customer Dashboard")
    #         self.master.geometry("")
    #         self.master.configure(bg="white")
    #
    #         # Create main frame for better organization
    #         self.main_frame = tk.Frame(self.master, bg="white")
    #         self.main_frame.pack(fill=tk.BOTH, expand=True)
    #
    #         # Logo / Branding
    #         self.logo_label = tk.Label(self.main_frame, text="EZRide", font=("Arial", 24, "bold"), fg="green",
    #                                    bg="white")
    #         self.logo_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
    #
    #         # Customer Info Frame (Pick-up, Drop-off, Date, Time)
    #         self.info_frame = tk.Frame(self.main_frame, bg="white")
    #         self.info_frame.grid(row=1, column=0, pady=20, padx=20, sticky="w")
    #
    #         # Pick-up Location
    #         self.pickup_label = tk.Label(self.info_frame, text="Pick-up Location", font=("Arial", 12), bg="white")
    #         self.pickup_label.grid(row=0, column=0, pady=5, sticky="w")
    #
    #         self.pickup_entry = tk.Entry(self.info_frame, font=("Arial", 12), width=40)
    #         self.pickup_entry.grid(row=0, column=1, pady=5)
    #
    #         # Drop-off Location
    #         self.dropoff_label = tk.Label(self.info_frame, text="Drop-off Location", font=("Arial", 12), bg="white")
    #         self.dropoff_label.grid(row=1, column=0, pady=5, sticky="w")
    #
    #         self.dropoff_entry = tk.Entry(self.info_frame, font=("Arial", 12), width=40)
    #         self.dropoff_entry.grid(row=1, column=1, pady=5)
    #
    #         # Date Picker for Booking Date
    #         self.booking_date_label = tk.Label(self.info_frame, text="Booking Date", font=("Arial", 12), bg="white")
    #         self.booking_date_label.grid(row=2, column=0, pady=5, sticky="w")
    #
    #         self.calendar = Calendar(self.info_frame, font=("Arial", 12), selectmode='day', date_pattern='yyyy-mm-dd')
    #         self.calendar.grid(row=2, column=1, pady=5)
    #
    #         # Time Picker for Booking Time
    #         self.booking_time_label = tk.Label(self.info_frame, text="Booking Time", font=("Arial", 12), bg="white")
    #         self.booking_time_label.grid(row=3, column=0, pady=5, sticky="w")
    #
    #         # Time Picker Components (Hour and Minute)
    #         self.time_frame = tk.Frame(self.info_frame, bg="white")
    #         self.time_frame.grid(row=3, column=1, pady=5, sticky="w")
    #
    #         self.time_hour = ttk.Combobox(self.time_frame, values=[f"{i:02}" for i in range(24)], font=("Arial", 12),
    #                                       width=5)
    #         self.time_hour.set("00")
    #         self.time_hour.grid(row=0, column=0, padx=5)
    #
    #         self.time_colon = tk.Label(self.time_frame, text=":", font=("Arial", 12), bg="white")
    #         self.time_colon.grid(row=0, column=1)
    #
    #         self.time_minute = ttk.Combobox(self.time_frame, values=[f"{i:02}" for i in range(60)], font=("Arial", 12),
    #                                         width=5)
    #         self.time_minute.set("00")
    #         self.time_minute.grid(row=0, column=2, padx=5)
    #
    #         # Buttons Section (Book, View, Cancel)
    #         self.button_frame = tk.Frame(self.main_frame, bg="white")
    #         self.button_frame.grid(row=2, column=0, pady=20, padx=20)
    #
    #         self.find_driver_button = tk.Button(self.button_frame, text="Book Taxi", font=("Arial", 12),
    #                                             command=self.book_taxi, bg="lightgreen", width=20)
    #         self.find_driver_button.grid(row=0, column=0, pady=10)
    #
    #         self.view_bookings_button = tk.Button(self.button_frame, text="View Bookings", font=("Arial", 12),
    #                                               command=self.view_bookings, bg="lightyellow", width=20)
    #         self.view_bookings_button.grid(row=1, column=0, pady=10)
    #
    #         self.cancel_booking_button = tk.Button(self.button_frame, text="Cancel Booking", font=("Arial", 12),
    #                                                command=self.cancel_booking, bg="lightcoral", width=20)
    #         self.cancel_booking_button.grid(row=2, column=0, pady=10)
    #
    #         # Map View Section
    #         self.map_button = tk.Button(self.main_frame, text="View on Google Maps", font=("Arial", 12),
    #                                     command=self.open_map, bg="lightblue", width=20)
    #         self.map_button.grid(row=3, column=0, pady=10, padx=20)
    #
    #         # Logout Button
    #         self.logout_button = tk.Button(self.main_frame, text="Logout", font=("Arial", 12), command=self.logout,
    #                                        bg="lightcoral", width=20)
    #         self.logout_button.grid(row=4, column=0, pady=20, padx=20)
    #
    #     def register(self):
    #         """
    #         Handles the customer registration functionality.
    #         """
    #         name = simpledialog.askstring("Name", "Enter your full name:")
    #         address = simpledialog.askstring("Address", "Enter your address:")
    #         phone_number = simpledialog.askstring("Phone Number", "Enter your phone number:")
    #         email = simpledialog.askstring("Email", "Enter your email:")
    #
    #         if not name or not address or not phone_number or not email:
    #             messagebox.showerror("Registration Error", "All fields are required!")
    #             return
    #
    #         # Store registration details in the database
    #         try:
    #             connection = create_connection()
    #             cursor = connection.cursor()
    #
    #             cursor.execute("""
    #                 INSERT INTO Customers (name, address, phone_number, email)
    #                 VALUES (%s, %s, %s, %s)
    #             """, (name, address, phone_number, email))
    #
    #             connection.commit()
    #             messagebox.showinfo("Registration Successful", f"Welcome, {name}! You can now book a taxi.")
    #         except Exception as e:
    #             messagebox.showerror("Database Error", f"Error during registration: {e}")
    #         finally:
    #             connection.close()
    #
    #     def book_taxi(self):
    #         """
    #         Handles the booking of a taxi.
    #         """
    #         pickup_location = self.pickup_entry.get()
    #         dropoff_location = self.dropoff_entry.get()
    #         booking_date = self.calendar.get_date()
    #         booking_time = f"{self.time_hour.get()}:{self.time_minute.get()}"
    #
    #         if not pickup_location or not dropoff_location or not booking_date or not booking_time:
    #             messagebox.showerror("Booking Error", "Please fill in all fields.")
    #             return
    #
    #         # Save booking to the database
    #         try:
    #             connection = create_connection()
    #             cursor = connection.cursor()
    #
    #             # Assuming customer_id = 1 for simplicity
    #             cursor.execute("""
    #                 INSERT INTO Bookings (customer_id, pickup_location, dropoff_location, booking_date, booking_time)
    #                 VALUES (%s, %s, %s, %s, %s)
    #             """, (1, pickup_location, dropoff_location, booking_date, booking_time))
    #
    #             connection.commit()
    #             messagebox.showinfo("Booking Successful", "Your taxi has been booked successfully!")
    #         except Exception as e:
    #             messagebox.showerror("Database Error", f"Error during booking: {e}")
    #         finally:
    #             connection.close()
    #
    #     def view_bookings(self):
    #         """
    #         Shows all bookings made by the customer.
    #         """
    #         try:
    #             connection = create_connection()
    #             cursor = connection.cursor()
    #
    #             cursor.execute("SELECT * FROM Bookings WHERE customer_id = 1")  # Example for customer_id = 1
    #             bookings = cursor.fetchall()
    #
    #             if bookings:
    #                 bookings_info = "\n".join([
    #                                               f"Booking ID: {booking[0]}, Pickup: {booking[2]}, Dropoff: {booking[3]}, Date: {booking[4]}, Time: {booking[5]}"
    #                                               for booking in bookings])
    #                 messagebox.showinfo("Your Bookings", bookings_info)
    #             else:
    #                 messagebox.showinfo("No Bookings", "You haven't made any bookings yet.")
    #         except Exception as e:
    #             messagebox.showerror("Database Error", f"Error fetching bookings: {e}")
    #         finally:
    #             connection.close()
    #
    #     def cancel_booking(self):
    #         """
    #         Cancels a booking.
    #         """
    #         booking_id = simpledialog.askinteger("Booking ID", "Enter the booking ID to cancel:")
    #
    #         if not booking_id:
    #             messagebox.showerror("Input Error", "Please enter a valid booking ID.")
    #             return
    #
    #         try:
    #             connection = create_connection()
    #             cursor = connection.cursor()
    #
    #             cursor.execute("DELETE FROM Bookings WHERE booking_id = %s AND customer_id = 1", (booking_id,))
    #             connection.commit()
    #
    #             messagebox.showinfo("Booking Canceled", "Your booking has been canceled successfully!")
    #         except Exception as e:
    #             messagebox.showerror("Database Error", f"Error canceling booking: {e}")
    #         finally:
    #             connection.close()
    #
    #     def open_map(self):
    #         """
    #         Opens Google Maps in a web browser to show the route from pickup to dropoff.
    #         """
    #         pickup_location = self.pickup_entry.get()
    #         dropoff_location = self.dropoff_entry.get()
    #
    #         if not pickup_location or not dropoff_location:
    #             messagebox.showerror("Error", "Please enter both pick-up and drop-off locations.")
    #             return
    #
    #         map_url = f"https://www.google.com/maps/dir/{pickup_location}/{dropoff_location}"
    #         webbrowser.open(map_url)
    #
    #     def logout(self):
    #         """
    #         Logs out and closes the application.
    #         """
    #         self.master.quit()
    #
    #
    # # Running the application
    # if __name__ == "__main__":
    #     root = tk.Tk()
    #     customer_dashboard = CustomerDashboard(root)
    #     root.mainloop()
