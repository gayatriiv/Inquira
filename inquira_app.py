import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

# Initialize the main window
root = tk.Tk()
root.title("INQUIRA - Find Collaborators")
root.geometry("400x500")
root.configure(bg="black")  # Set the background to black

# Set default font and colors
font_style = ("Garret", 12)
button_font = ("Garret", 10, "bold")
bg_color = "black"
fg_color = "white"
button_color = "#4CAF50"  # Green color for buttons

# Function to create the database
def create_db():
    conn = sqlite3.connect('devv.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
              id INTEGER PRIMARY KEY,
              username TEXT NOT NULL,
              email TEXT NOT NULL,
              password TEXT NOT NULL,
              bio TEXT,
              skills TEXT,
              experience TEXT,
              location TEXT,
              projects TEXT
              )''')
    c.execute('''CREATE TABLE IF NOT EXISTS connections (
              id INTEGER PRIMARY KEY,
              user_id INTEGER,
              target_user_id INTEGER,
              message TEXT,
              status TEXT,
              FOREIGN KEY (user_id) REFERENCES users (id),
              FOREIGN KEY (target_user_id) REFERENCES users (id)
              )''')
    conn.commit()
    conn.close()

create_db()

# Global variables
current_user_id = None
profile_exists = False

# Function to register a new user
def register_user():
    def save_user():
        username = entry_username.get()
        email = entry_email.get()
        password = entry_password.get()

        if username and email and password:
            conn = sqlite3.connect('devv.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                      (username, email, password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Registration successful!")
            register_window.destroy()
        else:
            messagebox.showerror("Error", "All fields must be filled!")

    register_window = tk.Toplevel(root)
    register_window.title("Register")
    register_window.configure(bg=bg_color)

    tk.Label(register_window, text="Username", font=font_style, fg=fg_color, bg=bg_color).grid(row=0, column=0)
    tk.Label(register_window, text="Email", font=font_style, fg=fg_color, bg=bg_color).grid(row=1, column=0)
    tk.Label(register_window, text="Password", font=font_style, fg=fg_color, bg=bg_color).grid(row=2, column=0)

    entry_username = tk.Entry(register_window, font=font_style)
    entry_email = tk.Entry(register_window, font=font_style)
    entry_password = tk.Entry(register_window, font=font_style, show='*')

    entry_username.grid(row=0, column=1)
    entry_email.grid(row=1, column=1)
    entry_password.grid(row=2, column=1)

    tk.Button(register_window, text="Register", font=button_font, bg=button_color, fg=fg_color, command=save_user).grid(row=3, column=1)

# Function to login user
def login_user():
    def check_login():
        global current_user_id
        email = entry_login_email.get()
        password = entry_login_password.get()

        conn = sqlite3.connect('devv.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            current_user_id = user[0]
            messagebox.showinfo("Success", "Login successful!")
            login_window.destroy()
            show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.configure(bg=bg_color)

    tk.Label(login_window, text="Email", font=font_style, fg=fg_color, bg=bg_color).grid(row=0, column=0)
    tk.Label(login_window, text="Password", font=font_style, fg=fg_color, bg=bg_color).grid(row=1, column=0)

    entry_login_email = tk.Entry(login_window, font=font_style)
    entry_login_password = tk.Entry(login_window, font=font_style, show='*')

    entry_login_email.grid(row=0, column=1)
    entry_login_password.grid(row=1, column=1)

    tk.Button(login_window, text="Login", font=button_font, bg=button_color, fg=fg_color, command=check_login).grid(row=2, column=1)

# Function to create or update user profile
def create_profile():
    def save_profile():
        bio = entry_bio.get()
        skills = entry_skills.get()
        experience = entry_experience.get()
        location = entry_location.get()
        projects = entry_projects.get()

        conn = sqlite3.connect('devv.db')
        c = conn.cursor()
        c.execute("UPDATE users SET bio=?, skills=?, experience=?, location=?, projects=? WHERE id=?",
                  (bio, skills, experience, location, projects, current_user_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Profile updated!")
        profile_window.destroy()

    profile_window = tk.Toplevel(root)
    profile_window.title("Create / Update Profile")
    profile_window.configure(bg=bg_color)

    tk.Label(profile_window, text="Bio", font=font_style, fg=fg_color, bg=bg_color).grid(row=0, column=0)
    tk.Label(profile_window, text="Skills", font=font_style, fg=fg_color, bg=bg_color).grid(row=1, column=0)
    tk.Label(profile_window, text="Experience", font=font_style, fg=fg_color, bg=bg_color).grid(row=2, column=0)
    tk.Label(profile_window, text="Location", font=font_style, fg=fg_color, bg=bg_color).grid(row=3, column=0)
    tk.Label(profile_window, text="Projects", font=font_style, fg=fg_color, bg=bg_color).grid(row=4, column=0)

    entry_bio = tk.Entry(profile_window, font=font_style)
    entry_skills = tk.Entry(profile_window, font=font_style)
    entry_experience = tk.Entry(profile_window, font=font_style)
    entry_location = tk.Entry(profile_window, font=font_style)
    entry_projects = tk.Entry(profile_window, font=font_style)

    entry_bio.grid(row=0, column=1)
    entry_skills.grid(row=1, column=1)
    entry_experience.grid(row=2, column=1)
    entry_location.grid(row=3, column=1)
    entry_projects.grid(row=4, column=1)

    tk.Button(profile_window, text="Save Profile", font=button_font, bg=button_color, fg=fg_color, command=save_profile).grid(row=5, column=1)

# Function to show dashboard options after login
def show_dashboard():
    dashboard_window = tk.Toplevel(root)
    dashboard_window.title("Dashboard")
    dashboard_window.configure(bg=bg_color)

    tk.Label(dashboard_window, text="Dashboard", font=("Garret", 24), fg=fg_color, bg=bg_color).pack(pady=20)

    tk.Button(dashboard_window, text="Create / Update Profile", font=button_font, bg=button_color, fg=fg_color, command=create_profile).pack(pady=10)
    tk.Button(dashboard_window, text="Search for Developers", font=button_font, bg=button_color, fg=fg_color, command=search_developers).pack(pady=10)
    tk.Button(dashboard_window, text="Send Connection Requests", font=button_font, bg=button_color, fg=fg_color, command=send_request).pack(pady=10)
    tk.Button(dashboard_window, text="View Connection Requests", font=button_font, bg=button_color, fg=fg_color, command=view_requests).pack(pady=10)
    
    # Add logout option
    tk.Button(dashboard_window, text="Logout", font=button_font, bg=button_color, fg=fg_color, command=logout).pack(pady=10)

# Function to search for developers by skills, location, and experience
def search_developers():
    search_window = tk.Toplevel(root)
    search_window.title("Search Developers")
    search_window.configure(bg=bg_color)

    tk.Label(search_window, text="Search by Skills, Location, Experience", font=font_style, fg=fg_color, bg=bg_color).grid(row=0, column=0)

    tk.Label(search_window, text="Skills", font=font_style, fg=fg_color, bg=bg_color).grid(row=1, column=0)
    tk.Label(search_window, text="Location", font=font_style, fg=fg_color, bg=bg_color).grid(row=2, column=0)
    tk.Label(search_window, text="Experience", font=font_style, fg=fg_color, bg=bg_color).grid(row=3, column=0)

    entry_search_skills = tk.Entry(search_window, font=font_style)
    entry_search_location = tk.Entry(search_window, font=font_style)
    entry_search_experience = tk.Entry(search_window, font=font_style)

    entry_search_skills.grid(row=1, column=1)
    entry_search_location.grid(row=2, column=1)
    entry_search_experience.grid(row=3, column=1)

    def perform_search():
        skills = entry_search_skills.get()
        location = entry_search_location.get()
        experience = entry_search_experience.get()

        query = "SELECT username, email, skills, location, experience FROM users WHERE 1=1"
        params = []

        if skills:
            query += " AND skills LIKE ?"
            params.append(f"%{skills}%")
        if location:
            query += " AND location LIKE ?"
            params.append(f"%{location}%")
        if experience:
            query += " AND experience LIKE ?"
            params.append(f"%{experience}%")

        conn = sqlite3.connect('devv.db')
        c = conn.cursor()
        c.execute(query, params)
        results = c.fetchall()
        conn.close()

        result_window = tk.Toplevel(search_window)
        result_window.title("Search Results")
        result_window.configure(bg=bg_color)

        tk.Label(result_window, text="Search Results", font=("Garret", 20), fg=fg_color, bg=bg_color).pack(pady=20)

        if results:
            for result in results:
                tk.Label(result_window, text=f"Username: {result[0]}, Skills: {result[2]}, Location: {result[3]}, Experience: {result[4]}, Email: {result[1]}", font=font_style, fg=fg_color, bg=bg_color).pack(pady=5)
        else:
            messagebox.showinfo("No Results", "No developers found with those criteria.")

    tk.Button(search_window, text="Search", font=button_font, bg=button_color, fg=fg_color, command=perform_search).grid(row=4, column=1)

# Function to send connection request
def send_request():
    def send():
        target_user_email = entry_target_email.get()
        message = entry_message.get()

        if target_user_email and message:
            conn = sqlite3.connect('devv.db')
            c = conn.cursor()
            c.execute("SELECT id FROM users WHERE email=?", (target_user_email,))
            target_user = c.fetchone()

            if target_user:
                target_user_id = target_user[0]
                c.execute("INSERT INTO connections (user_id, target_user_id, message, status) VALUES (?, ?, ?, ?)",
                          (current_user_id, target_user_id, message, "Pending"))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Connection request sent!")
                request_window.destroy()
            else:
                messagebox.showerror("Error", "User not found!")
        else:
            messagebox.showerror("Error", "Please fill in all fields!")

    request_window = tk.Toplevel(root)
    request_window.title("Send Connection Request")
    request_window.configure(bg=bg_color)

    tk.Label(request_window, text="Target User Email", font=font_style, fg=fg_color, bg=bg_color).grid(row=0, column=0)
    tk.Label(request_window, text="Message", font=font_style, fg=fg_color, bg=bg_color).grid(row=1, column=0)

    entry_target_email = tk.Entry(request_window, font=font_style)
    entry_message = tk.Entry(request_window, font=font_style)

    entry_target_email.grid(row=0, column=1)
    entry_message.grid(row=1, column=1)

    tk.Button(request_window, text="Send Request", font=button_font, bg=button_color, fg=fg_color, command=send).grid(row=2, column=1)

# Function to view connection requests
def view_requests():
    conn = sqlite3.connect('devv.db')
    c = conn.cursor()
    c.execute("SELECT u.username, c.message, c.status FROM connections c JOIN users u ON c.user_id = u.id WHERE c.target_user_id=?", (current_user_id,))
    requests = c.fetchall()
    conn.close()

    request_view_window = tk.Toplevel(root)
    request_view_window.title("Connection Requests")
    request_view_window.configure(bg=bg_color)

    tk.Label(request_view_window, text="Your Connection Requests", font=("Garret", 20), fg=fg_color, bg=bg_color).pack(pady=20)

    for req in requests:
        tk.Label(request_view_window, text=f"From: {req[0]}, Message: {req[1]}, Status: {req[2]}", font=font_style, fg=fg_color, bg=bg_color).pack(pady=5)

# Function to logout
def logout():
    global current_user_id
    current_user_id = None
    messagebox.showinfo("Logged Out", "You have been logged out!")
    root.quit()

# Set up the main login/register interface
tk.Label(root, text="Welcome to INQUIRA", font=("Garret", 24), fg=fg_color, bg=bg_color).pack(pady=20)
tk.Button(root, text="Register", font=button_font, bg=button_color, fg=fg_color, command=register_user).pack(pady=10)
tk.Button(root, text="Login", font=button_font, bg=button_color, fg=fg_color, command=login_user).pack(pady=10)

root.mainloop()
