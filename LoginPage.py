import tkinter as tk
from tkinter import messagebox
from DatabaseConnection import create_connection
from CustomerDashboard import CustomerDashboard  # Import customer dashboard function
from DriverDashboard import DriverDashboard  # Import driver dashboard function
from AdminDashboard import AdminDashboard  # Import admin dashboard function

def authenticate_user(master):


    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showwarning("Input Error", "Username and password are required!")
        return

    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT user_role, user_id, username, password_hash FROM LoginCredentials WHERE username = %s",
            (username,)
        )
        user = cursor.fetchone()

        if user:
            user_role, user_id, db_username, db_password = user
            if password == db_password:  # In production, you should hash the password and compare hashes
                if user_role == "Customer":
                    CustomerDashboard(root=master)
                elif user_role == "Driver":
                    DriverDashboard(user_id)
                elif user_role == "Admin":
                    AdminDashboard()
                else:
                    messagebox.showerror("Login Error", "Unknown user role!")
            else:
                messagebox.showerror("Login Error", "Invalid username or password!")
        else:
            messagebox.showerror("Login Error", "Invalid username or password!")

    except Exception as e:
        messagebox.showerror("Database Error", f"Error occurred: {e}")

    finally:
        connection.close()

def custom():
    print("Login_button_clicked")

root = tk.Tk()
root.title("EZride - Login Page")
root.geometry("500x500")
root.configure(bg="#f4f4f9")

header = tk.Label(root, text="EZride", font=("Arial", 24, "bold"), bg="#4CAF50", fg="black", pady=10)
header.pack(fill="x")

# Username
tk.Label(root, text="Username:", font=("Arial", 12), bg="#f4f4f9").pack(pady=5)
username_entry = tk.Entry(root, font=("Arial", 12), width=30)
username_entry.pack(pady=5)

# Password
tk.Label(root, text="Password:", font=("Arial", 12), bg="#f4f4f9").pack(pady=5)
password_entry = tk.Entry(root, font=("Arial", 12), show="*", width=30)
password_entry.pack(pady=5)

# Login Button
login_button = tk.Button(root, text="Login", font=("Arial", 12), bg="#4CAF50", fg="black", command=lambda:authenticate_user(root))
login_button.pack(pady=20)

login_button = tk.Button(root, text="Sign up", font=("Arial", 12), bg="#4CAF50", fg="black", command=lambda:signup(root))
login_button.pack(pady=20)


def signup(master):
    root.destroy()
    from SignUpPage import display_form
    display_form(master)

root.mainloop()