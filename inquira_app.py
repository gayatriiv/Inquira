import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class InquiraApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("INQUIRA")
        self.geometry("800x600")

        self.current_user = None

        # Create database connection
        self.conn = sqlite3.connect('inquira.db')
        self.create_tables()

        # Create and show the login frame
        self.show_login()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                required_skills TEXT,
                user_id INTEGER,
                status TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.conn.commit()

    def show_login(self):
        login_frame = ttk.Frame(self)
        login_frame.pack(padx=10, pady=10)

        ttk.Label(login_frame, text="Username:").grid(row=0, column=0, sticky="e")
        self.username_entry = ttk.Entry(login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, sticky="e")
        self.password_entry = ttk.Entry(login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(login_frame, text="Register", command=self.show_register).grid(row=3, column=0, columnspan=2)

    def show_register(self):
        register_frame = ttk.Frame(self)
        register_frame.pack(padx=10, pady=10)

        ttk.Label(register_frame, text="Username:").grid(row=0, column=0, sticky="e")
        self.reg_username_entry = ttk.Entry(register_frame)
        self.reg_username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(register_frame, text="Email:").grid(row=1, column=0, sticky="e")
        self.reg_email_entry = ttk.Entry(register_frame)
        self.reg_email_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(register_frame, text="Password:").grid(row=2, column=0, sticky="e")
        self.reg_password_entry = ttk.Entry(register_frame, show="*")
        self.reg_password_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(register_frame, text="Register", command=self.register).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(register_frame, text="Back to Login", command=self.show_login).grid(row=4, column=0, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            self.current_user = user
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def register(self):
        username = self.reg_username_entry.get()
        email = self.reg_email_entry.get()
        password = self.reg_password_entry.get()

        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
            self.conn.commit()
            messagebox.showinfo("Registration Successful", "You can now log in with your new account")
            self.show_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Registration Failed", "Username or email already exists")

    def show_dashboard(self):
        # Clear current window
        for widget in self.winfo_children():
            widget.destroy()

        dashboard_frame = ttk.Frame(self)
        dashboard_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        ttk.Label(dashboard_frame, text=f"Welcome, {self.current_user[1]}!", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        # Project List
        ttk.Label(dashboard_frame, text="Your Projects", font=("Arial", 14)).grid(row=1, column=0, sticky="w", pady=5)
        project_list = ttk.Treeview(dashboard_frame, columns=("Name", "Status"), show="headings")
        project_list.heading("Name", text="Project Name")
        project_list.heading("Status", text="Status")
        project_list.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Populate project list
        self.populate_project_list(project_list)

        # Action Buttons
        button_frame = ttk.Frame(dashboard_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Search Projects", command=self.search_projects).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Create Project", command=self.create_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Messages", command=self.show_messages).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Profile", command=self.edit_profile).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Logout", command=self.logout).pack(side=tk.LEFT, padx=5)

        # Make the dashboard resizable
        dashboard_frame.columnconfigure(0, weight=1)
        dashboard_frame.rowconfigure(2, weight=1)

    def populate_project_list(self, project_list):
        # Fetch projects from the database and populate the list
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, status FROM projects WHERE user_id = ?", (self.current_user[0],))
        projects = cursor.fetchall()

        for project in projects:
            project_list.insert("", tk.END, values=project)

    def search_projects(self):
        search_window = tk.Toplevel(self)
        search_window.title("Search Projects")

        ttk.Label(search_window, text="Keyword:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        keyword_entry = ttk.Entry(search_window)
        keyword_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(search_window, text="Skills:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        skills_entry = ttk.Entry(search_window)
        skills_entry.grid(row=1, column=1, padx=5, pady=5)

        results_tree = ttk.Treeview(search_window, columns=("Name", "Skills", "Status"), show="headings")
        results_tree.heading("Name", text="Project Name")
        results_tree.heading("Skills", text="Required Skills")
        results_tree.heading("Status", text="Status")
        results_tree.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        def perform_search():
            keyword = keyword_entry.get()
            skills = skills_entry.get()

            cursor = self.conn.cursor()
            query = """
                SELECT name, required_skills, status 
                FROM projects 
                WHERE (name LIKE ? OR description LIKE ?) 
                AND (required_skills LIKE ? OR ? = '')
                AND status = 'Open'
            """
            cursor.execute(query, (f"%{keyword}%", f"%{keyword}%", f"%{skills}%", skills))
            results = cursor.fetchall()

            results_tree.delete(*results_tree.get_children())
            for result in results:
                results_tree.insert("", tk.END, values=result)

        ttk.Button(search_window, text="Search", command=perform_search).grid(row=3, column=0, columnspan=2, pady=10)

        # Make the search window resizable
        search_window.columnconfigure(1, weight=1)
        search_window.rowconfigure(2, weight=1)

    def create_project(self):
        create_window = tk.Toplevel(self)
        create_window.title("Create New Project")

        ttk.Label(create_window, text="Project Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_entry = ttk.Entry(create_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(create_window, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        desc_entry = ttk.Text(create_window, height=3, width=30)
        desc_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(create_window, text="Required Skills:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        skills_entry = ttk.Entry(create_window)
        skills_entry.grid(row=2, column=1, padx=5, pady=5)

        def save_project():
            name = name_entry.get()
            description = desc_entry.get("1.0", tk.END).strip()
            skills = skills_entry.get()

            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO projects (name, description, required_skills, user_id, status)
                VALUES (?, ?, ?, ?, ?)
            """, (name, description, skills, self.current_user[0], "Open"))
            self.conn.commit()

            messagebox.showinfo("Success", "Project created successfully!")
            create_window.destroy()
            self.show_dashboard()  # Refresh the dashboard to show the new project

        ttk.Button(create_window, text="Create Project", command=save_project).grid(row=3, column=0, columnspan=2, pady=10)

    def show_messages(self):
        # Implement messaging system
        pass

    def edit_profile(self):
        # Implement profile editing functionality
        pass

    def logout(self):
        self.current_user = None
        self.show_login()

if __name__ == "__main__":
    app = InquiraApp()
    app.mainloop()