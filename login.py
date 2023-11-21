import tkinter as tk
import mysql.connector
from PIL import Image, ImageTk
import os
from tkinter import messagebox

mydb = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="projectksksk"
)

# Create a cursor for executing SQL queries
cursor = mydb.cursor()

def check_login_credentials(email, password):
    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    result = cursor.fetchone()
    return result is not None


def create_login_box(event=None):
    root.destroy()
    new_window = tk.Tk()
    new_window.geometry('250x500')
    new_window.title('Login')
    global email_entry, password_entry, login_window, signup_box  # Make signup_box global
    login_box = tk.Frame(new_window, borderwidth=2, relief="ridge", padx=10, pady=10)
    login_box.pack(padx=20, pady=20)

    email_label = tk.Label(login_box, text="Email Address:")
    email_label.pack(anchor="w")
    email_entry = tk.Entry(login_box)
    email_entry.pack(fill="x", padx=10, pady=5)

    password_label = tk.Label(login_box, text="Password:")
    password_label.pack(anchor="w")
    password_entry = tk.Entry(login_box, show="*")
    password_entry.pack(fill="x", padx=10, pady=5)

    login_button = tk.Button(login_box, text="Login", command=login)
    login_button.pack(pady=10)

    admin_login_button = tk.Button(new_window, borderwidth=2, relief="ridge", padx=10, pady=10, bg='lightgreen', text="Login as Admin", command=None)
    admin_login_button.pack(pady=10)


    def homepage():
        new_window.destroy()
        os.system('python login.py')

    homepage_button = tk.Button(login_box, text="Back to Homepage", command=homepage)
    homepage_button.pack(pady=10)

    # Hide the signup_box if it exists
    #if signup_box:
        #signup_box.pack_forget()

    # Initialize the signup_box as None
    #signup_box = None

def login():
    global email_entry, password_entry
    email = email_entry.get()
    password = password_entry.get()
    if email and password:
        if check_login_credentials(email, password):
            # Retrieve user information from the database based on the email
            query = "SELECT full_name, age, sex FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user_info = cursor.fetchone()
            
            if user_info:
                full_name, age, sex = user_info
                root.destroy()
                os.system('python appointment.py')
            else:
                messagebox.showerror("Login Failed", "Invalid email or password")
        else:
            messagebox.showerror("Login Failed", "Invalid email or password")
    else:
        messagebox.showerror("Invalid Information", "Please fill in both email and password.")




# Create the main window
root = tk.Tk()
root.geometry("1360x760")
root.title("Hospital Management System")

# Load and display the background image
background_image = Image.open("C:/Users/Chloie/Documents/project/homepage.png")
background_image = background_image.resize((1350, 730), Image.Resampling.NEAREST)
background_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create buttons for admin login, regular login, sign up, and HMS info
admin_login_button = tk.Button(root, text="Admin Login", command=None)
admin_login_button.pack(side="right", anchor="ne", padx=10, pady=10)

user_login_button = tk.Button(root, text="User Login", command=create_login_box)
user_login_button.pack(side="right", anchor="ne", padx=10, pady=10)

signup_button = tk.Button(root, text="Sign Up", command=None)
signup_button.pack(side="right", anchor="ne", padx=10, pady=10)

hms_info_button = tk.Button(root, text="About HMS", command=None)
hms_info_button.pack(side="right", anchor="ne", padx=10, pady=10)

root.mainloop()
