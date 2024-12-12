import tkinter as tk
from doctest import master
from tkinter import messagebox
from tkinter import ttk
import re
from DatabaseConnection import create_connection  # Ensure you have a database connection module


def is_valid_email(email):
    """Validate email using regex."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

def save_to_database(user_type):

    connection = create_connection()
    cursor = connection.cursor()

    try:
        if user_type == "Customer":

            name = name_entry.get()
            address = address_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()
            username = username_entry.get()
            password = password_entry.get()

            if not all([name, phone, email, username, password]):  # Basic validation
                messagebox.showwarning("Input Error", "All fields are required!")
                return

            if not is_valid_email(email):
                messagebox.showerror("Input Error", "Invalid email format!")
                return

            # Insert into Customers table
            cursor.execute(
                "INSERT INTO Customers (name, address, phone_number, email) VALUES (%s, %s, %s, %s)",
                (name, address, phone, email)
            )
            customer_id = cursor.lastrowid  # Get the auto-generated customer_id

            # Insert into LoginCredentials table
            cursor.execute(
                "INSERT INTO LoginCredentials (user_role, user_id, username, password_hash) VALUES (%s, %s, %s, %s)",
                ("Customer", customer_id, username, password)
            )

        elif user_type == "Driver":
            # Collect Driver data
            name = name_entry.get()
            phone = phone_entry.get()
            numberplate = numberplate_entry.get()
            availability = availability_var.get()
            username = username_entry.get()
            password = password_entry.get()

            if not all([name, phone, numberplate, username, password]):  # Basic validation
                messagebox.showwarning("Input Error", "All fields are required!")
                return

            # Insert into Drivers table
            cursor.execute(
                "INSERT INTO Drivers (name, phone_number, numberplate_color, availability_status) VALUES (%s, %s, %s, %s)",
                (name, phone, numberplate, availability)
            )
            driver_id = cursor.lastrowid

            # Insert into LoginCredentials table
            cursor.execute(
                "INSERT INTO LoginCredentials (user_role, user_id, username, password_hash) VALUES (%s, %s, %s, %s)",
                ("Driver", driver_id, username, password)
            )

        # Commit changes to the database
        connection.commit()
        messagebox.showinfo("Success", f"{user_type} registered successfully!")

    except Exception as e:
        connection.rollback()
        messagebox.showerror("Database Error", f"Error occurred: {e}")
    finally:
        connection.close()


def display_form(user_type):

    # Clear the current form
    for widget in form_frame.winfo_children():
        widget.destroy()

    # Common fields for both Customer and Driver
    tk.Label(form_frame, text="Name:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5, padx=10)
    global name_entry
    name_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    name_entry.grid(row=0, column=1, pady=5, padx=10)

    tk.Label(form_frame, text="Phone Number:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5, padx=10)
    global phone_entry
    phone_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    phone_entry.grid(row=1, column=1, pady=5, padx=10)

    tk.Label(form_frame, text="Username:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5, padx=10)
    global username_entry
    username_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    username_entry.grid(row=2, column=1, pady=5, padx=10)

    tk.Label(form_frame, text="Password:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", pady=5, padx=10)
    global password_entry
    password_entry = tk.Entry(form_frame, font=("Arial", 12), show="*", width=30)
    password_entry.grid(row=3, column=1, pady=5, padx=10)

    if user_type == "Customer":
        tk.Label(form_frame, text="Address:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", pady=5, padx=10)
        global address_entry
        address_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
        address_entry.grid(row=4, column=1, pady=5, padx=10)

        tk.Label(form_frame, text="Email:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", pady=5, padx=10)
        global email_entry
        email_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
        email_entry.grid(row=5, column=1, pady=5, padx=10)

        submit_button = tk.Button(form_frame, text="Register as Customer", font=("Arial", 12), bg="white", fg="black",
                                  command=lambda: save_to_database("Customer"))
        submit_button.grid(row=6, column=0, columnspan=2, pady=15)

    elif user_type == "Driver":
        tk.Label(form_frame, text="Vehicle Number and Color:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", pady=5, padx=10)
        global numberplate_entry
        numberplate_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
        numberplate_entry.grid(row=4, column=1, pady=5, padx=10)

        tk.Label(form_frame, text="Availability Status:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", pady=5, padx=10)
        global availability_var
        availability_var = tk.BooleanVar()
        availability_checkbox = tk.Checkbutton(form_frame, text="Available", variable=availability_var, font=("Arial", 12))
        availability_checkbox.grid(row=5, column=1, sticky="w", pady=5, padx=10)

        submit_button = tk.Button(form_frame, text="Register as Driver", font=("Arial", 12), bg="white", fg="black",
                                  command=lambda: save_to_database("Driver"))
        submit_button.grid(row=6, column=0, columnspan=2, pady=15)


# Create the main signup window
root = tk.Tk()
root.title("EZride - Signup Page")
root.geometry("600x600")
root.configure(bg="#f4f4f9")

# Company Name
header = tk.Label(root, text="EZride", font=("Arial", 24, "bold"), bg="black", fg="white", pady=10)
header.pack(fill="x")

# User Type Selection
user_type_frame = tk.Frame(root, bg="#f4f4f9")
user_type_frame.pack(pady=20)
tk.Label(user_type_frame, text="Are you a:", font=("Arial", 14), bg="#f4f4f9").pack(side="left", padx=5)
user_type_combobox = ttk.Combobox(user_type_frame, values=["Customer", "Driver"], state="readonly", font=("Arial", 12))
user_type_combobox.pack(side="left", padx=5)

select_button = tk.Button(user_type_frame, text="Select", font=("Arial", 12), bg="black", fg="white",
                          command=lambda: display_form(user_type_combobox.get()))
select_button.pack(side="left", padx=5)

# Dynamic Form Frame
form_frame = tk.Frame(root, bg="#f4f4f9")
form_frame.pack(pady=10)

# Login Page Button
login_button = tk.Button(root, text="Back to login", font=("Arial", 12), bg="black", fg="white", command=lambda: login(root))
login_button.pack(pady=20)

def login(root):
    root.destroy()
    from LoginPage import custom
    custom()
# Run the Tkinter event loop
root.mainloop()