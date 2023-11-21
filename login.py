import tkinter as tk
import mysql.connector
from PIL import Image, ImageTk
import os
from tkinter import messagebox
import re

###########################################################################

# Maximum appointments per doctor's slot
MAX_APPOINTMENTS_PER_SLOT = 2

# Declare global variables
search_date_entry = None
search_time_var = None
search_doctor_var = None
date_entry = None

# Add these global variables at the beginning of your code
name_var = None
date_var = None
time_var = None
search_date_entry = None
patient_name = None
age = None
contact_number = None
sex = None
selected_reason = None
disease = None
selected_doctor = None
appointment_time = None
appointment_date = None
amount = None

####################################################################################

mydb = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="projectksksk"
)

# Create a cursor for executing SQL queries
cursor = mydb.cursor()
###########################################################################################################3
def insert_users_into_db(full_name, age, sex, email, password):
    try:
        query = "INSERT INTO users (full_name, age, sex, email, password) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (full_name, age, sex, email, password))
        mydb.commit()
        return True
    except Exception as e:
        print("Error while inserting into the database:", str(e))
        mydb.rollback()
        return False
#########################################################################################
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
    root.destroy()
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

# Function to display About HMS window
def hms_info():
    about_window = tk.Toplevel(root)
    about_window.title("About HMS")
    about_window.geometry("400x200")
    label = tk.Label(about_window, text="This is the Hospital Management System (HMS).")
    label.pack(pady=20)
    ok_button = tk.Button(about_window, text="OK", command=homepage)
    ok_button.pack()

    def homepage():
            about_window.destroy()
            os.system('python login.py')

#############################3
def signup():
    global full_name, age, sex
    #full_name = full_name_entry.get()
    #age = age_entry.get()
    #sex = sex_var.get()
    #email = email_entry.get()
    #password = password_entry.get()
    #if  "@gmail.com" not in email:
     #   messagebox.showerror("Invalid Email", "Please enter a valid Gmail address.")
      #  return
    #i3f full_name and age and sex and email and password:
     #   if insert_users_into_db(full_name, age, sex, email, password):
      #      messagebox.showinfo("Signup Successful", "Account created successfully!")
            #appointment_window(full_name, age, sex)
       # else:
        #    messagebox.showerror("Signup Failed", "Failed to create an account. Please try again.")
    #else:
     #   messagebox.showerror("Invalid Information", "Please fill in all the information needed.")

    ok_button = tk.Button(create_signup_box, text="OK", command=homepage)
    ok_button.pack()

    def homepage():
            create_signup_box.destroy()
            os.system('python login.py')
#######################

##############################################

def create_signup_box():
    global full_name_entry, age_entry, sex_var, email_entry, password_entry, signup_box
    signup_box = tk.Frame(root, borderwidth=2, relief="ridge", padx=10, pady=10, bg='lightblue')
    signup_box.pack(padx=10, pady=8)

    full_name_label = tk.Label(signup_box, text="Full Name:", anchor="w", bg='lightblue')
    full_name_label.pack()
    full_name_entry = tk.Entry(signup_box)
    full_name_entry.pack(fill="x", padx=10, pady=5)

    age_label = tk.Label(signup_box, text="Age:", anchor="w", bg='lightblue')
    age_label.pack()
    age_entry = tk.Entry(signup_box)
    age_entry.pack(fill="x", padx=10, pady=5)

    sex_label = tk.Label(signup_box, text="Sex:", anchor="w", bg='lightblue')
    sex_label.pack()
    sex_var = tk.StringVar(value="Male")
    sex_radio_male = tk.Radiobutton(signup_box, text="Male", variable=sex_var, value="Male", bg='lightblue')
    sex_radio_female = tk.Radiobutton(signup_box, text="Female", variable=sex_var, value="Female", bg='lightblue')
    sex_radio_male.pack()
    sex_radio_female.pack()

    email_label = tk.Label(signup_box, text="Email Address:", anchor="w", bg='lightblue')
    email_label.pack()
    email_entry = tk.Entry(signup_box)
    email_entry.pack(fill="x", padx=10, pady=5)

    password_label = tk.Label(signup_box, text="Password:", anchor="w", bg='lightblue')
    password_label.pack()
    password_entry = tk.Entry(signup_box, show="*")
    password_entry.pack(fill="x", padx=10, pady=5)

    create_acc_button = tk.Button(signup_box, text="Create Account", bg='lightgreen', command=signup)
    create_acc_button.pack(pady=10)

    login_page_button = tk.Label(signup_box, text="Already have an account? Log in here.", fg='blue', cursor='hand2', bg='lightblue')
    login_page_button.bind("<Button-1>", create_login_box)
    login_page_button.pack()


def is_valid_email(email):
    # Define a regular expression pattern to validate Gmail addresses
    gmail_pattern = r'^[\w\.-]+@gmail\.com$'
    return bool(re.match(gmail_pattern, email))

###############################################

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

signup_button = tk.Button(root, text="Sign Up", command=create_signup_box)
signup_button.pack(side="right", anchor="ne", padx=10, pady=10)

hms_info_button = tk.Button(root, text="About HMS", command=hms_info)
hms_info_button.pack(side="right", anchor="ne", padx=10, pady=10)

root.mainloop()
