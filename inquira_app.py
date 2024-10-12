import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

# Initialize the main window
root = tk.Tk()
root.title("INQUIRA - Find Collaborators")
root.geometry("400x500")

# Database setup
def create_db():
    conn = sqlite3.connect('devv.db')  # Changed to devv.db
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

# Function to register a new user
def register_user():
    def save_user():
        username = entry_username.get()
        email = entry_email.get()
        password = entry_password.get()

        if username and email and password:
            conn = sqlite3.connect('devv.db')  # Changed to devv.db
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

    tk.Label(register_window, text="Username").grid(row=0, column=0)
    tk.Label(register_window, text="Email").grid(row=1, column=0)
    tk.Label(register_window, text="Password").grid(row=2, column=0)

    entry_username = tk.Entry(register_window)
    entry_email = tk.Entry(register_window)
    entry_password = tk.Entry(register_window, show='*')

    entry_username.grid(row=0, column=1)
    entry_email.grid(row=1, column=1)
    entry_password.grid(row=2, column=1)

    tk.Button(register_window, text="Register", command=save_user).grid(row=3, column=1)

# Function to login user
def login_user():
    def check_login():
        global current_user_id
        email = entry_login_email.get()
        password = entry_login_password.get()

        conn = sqlite3.connect('devv.db')  # Changed to devv.db
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            current_user_id = user[0]
            messagebox.showinfo("Success", "Login successful!")
            login_window.destroy()
            show_main_window()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    login_window = tk.Toplevel(root)
    login_window.title("Login")

    tk.Label(login_window, text="Email").grid(row=0, column=0)
    tk.Label(login_window, text="Password").grid(row=1, column=0)

    entry_login_email = tk.Entry(login_window)
    entry_login_password = tk.Entry(login_window, show='*')

    entry_login_email.grid(row=0, column=1)
    entry_login_password.grid(row=1, column=1)

    tk.Button(login_window, text="Login", command=check_login).grid(row=2, column=1)

# Function to create or update user profile
def create_profile():
    def save_profile():
        bio = entry_bio.get()
        skills = entry_skills.get()
        experience = entry_experience.get()
        location = entry_location.get()
        projects = entry_projects.get()

        conn = sqlite3.connect('devv.db')  # Changed to devv.db
        c = conn.cursor()
        c.execute("UPDATE users SET bio=?, skills=?, experience=?, location=?, projects=? WHERE id=?",
                  (bio, skills, experience, location, projects, current_user_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Profile updated!")
        profile_window.destroy()

    profile_window = tk.Toplevel(root)
    profile_window.title("Create Profile")

    tk.Label(profile_window, text="Bio").grid(row=0, column=0)
    tk.Label(profile_window, text="Skills").grid(row=1, column=0)
    tk.Label(profile_window, text="Experience").grid(row=2, column=0)
    tk.Label(profile_window, text="Location").grid(row=3, column=0)
    tk.Label(profile_window, text="Projects").grid(row=4, column=0)

    entry_bio = tk.Entry(profile_window)
    entry_skills = tk.Entry(profile_window)
    entry_experience = tk.Entry(profile_window)
    entry_location = tk.Entry(profile_window)
    entry_projects = tk.Entry(profile_window)

    entry_bio.grid(row=0, column=1)
    entry_skills.grid(row=1, column=1)
    entry_experience.grid(row=2, column=1)
    entry_location.grid(row=3, column=1)
    entry_projects.grid(row=4, column=1)

    tk.Button(profile_window, text="Save Profile", command=save_profile).grid(row=5, column=1)

# Function to view and manage connections
def view_connections():
    conn_window = tk.Toplevel(root)
    conn_window.title("Connection Requests")

    def manage_request(request_id, action):
        conn = sqlite3.connect('devv.db')  # Changed to devv.db
        c = conn.cursor()
        c.execute("UPDATE connections SET status=? WHERE id=?", (action, request_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Connection request {action}!")
        conn_window.destroy()

    conn = sqlite3.connect('devv.db')  # Changed to devv.db
    c = conn.cursor()
    c.execute("SELECT * FROM connections WHERE target_user_id=? AND status=?", (current_user_id, 'pending'))
    requests = c.fetchall()
    conn.close()

    if not requests:
        tk.Label(conn_window, text="No incoming requests").grid(row=0, column=0)
    else:
        for i, request in enumerate(requests):
            tk.Label(conn_window, text=f"From: {request[1]}, Message: {request[3]}").grid(row=i, column=0)
            tk.Button(conn_window, text="Accept", command=lambda req_id=request[0]: manage_request(req_id, 'accepted')).grid(row=i, column=1)
            tk.Button(conn_window, text="Decline", command=lambda req_id=request[0]: manage_request(req_id, 'declined')).grid(row=i, column=2)

# Function to send connection request
def send_connection():
    target_email = simpledialog.askstring("Input", "Enter the email of the user you want to connect with:")

    if target_email:
        message = simpledialog.askstring("Input", "Enter your message:")
        conn = sqlite3.connect('devv.db')  # Changed to devv.db
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE email=?", (target_email,))
        target_user = c.fetchone()

        if target_user:
            c.execute("INSERT INTO connections (user_id, target_user_id, message, status) VALUES (?, ?, ?, ?)", (current_user_id, target_user[0], message, 'pending'))
            conn.commit()
            messagebox.showinfo("Success", "Connection request sent!")
        else:
            messagebox.showerror("Error", "User not found!")
        conn.close()

# Function to search for profiles
def search_profiles():
    search_window = tk.Toplevel(root)
    search_window.title("Search Profiles")

    def perform_search():
        skills = entry_search_skills.get()
        experience = entry_search_experience.get()
        location = entry_search_location.get()
        projects = entry_search_projects.get()

        conn = sqlite3.connect('devv.db')  # Changed to devv.db
        c = conn.cursor()
        c.execute("SELECT username, skills, experience, location, projects FROM users WHERE skills LIKE ? AND experience LIKE ? AND location LIKE ? AND projects LIKE ?", 
                  (f'%{skills}%', f'%{experience}%', f'%{location}%', f'%{projects}%'))
        results = c.fetchall()
        conn.close()

        result_text.delete(1.0, tk.END)
        for result in results:
            result_text.insert(tk.END, f"Username: {result[0]}, Skills: {result[1]}, Experience: {result[2]}, Location: {result[3]}, Projects: {result[4]}\n")

    tk.Label(search_window, text="Search by Skills").grid(row=0, column=0)
    tk.Label(search_window, text="Search by Experience").grid(row=1, column=0)
    tk.Label(search_window, text="Search by Location").grid(row=2, column=0)
    tk.Label(search_window, text="Search by Projects").grid(row=3, column=0)

    entry_search_skills = tk.Entry(search_window)
    entry_search_experience = tk.Entry(search_window)
    entry_search_location = tk.Entry(search_window)
    entry_search_projects = tk.Entry(search_window)

    entry_search_skills.grid(row=0, column=1)
    entry_search_experience.grid(row=1, column=1)
    entry_search_location.grid(row=2, column=1)
    entry_search_projects.grid(row=3, column=1)

    tk.Button(search_window, text="Search", command=perform_search).grid(row=4, column=1)

    result_text = tk.Text(search_window, height=10, width=50)
    result_text.grid(row=5, column=0, columnspan=2)

# Function to show the main window after logging in
def show_main_window():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Welcome to INQUIRA", font=("Arial", 16)).pack(pady=20)

    tk.Button(root, text="Create Profile", command=create_profile).pack(pady=10)
    tk.Button(root, text="Search for Developers", command=search_profiles).pack(pady=10)
    tk.Button(root, text="View Connections", command=view_connections).pack(pady=10)
    tk.Button(root, text="Send Connection Request", command=send_connection).pack(pady=10)

    # Logout Button
    tk.Button(root, text="Logout", command=logout).pack(pady=10)

# Logout functionality
def logout():
    global current_user_id
    current_user_id = None
    messagebox.showinfo("Logout", "You have been logged out.")
    show_login_screen()

# Show login screen initially
def show_login_screen():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="INQUIRA - Login", font=("Arial", 16)).pack(pady=20)
    tk.Button(root, text="Login", command=login_user).pack(pady=10)
    tk.Button(root, text="Register", command=register_user).pack(pady=10)

# Start with login screen
show_login_screen()

# Start the Tkinter main loop
root.mainloop()
