# INQUIRA

**INQUIRA** is a **developer networking platform** designed to connect programmers and professionals for collaborative projects. Users can create profiles, search for other developers based on skills, experience, and location, send connection requests, and manage connections—all in a user-friendly interface.

## Features
- **User Authentication**: Secure registration and login system.
- **Profile Creation & Management**: Users can create, edit, and manage detailed profiles highlighting skills, experience, and location.
- **Advanced Search and Filters**: Filter potential collaborators by skills, experience, and location.
- **Connection Requests**: Users can send and manage connection requests with personalized messages.
- **Theme Toggle**: Option to switch between light and dark themes for a comfortable user experience.

## Technologies
- **Frontend**: Advanced web development 
- **Backend**: Python
- **Database**: SQLite for local development, scalable to other relational databases

## Getting Started

### Prerequisites
- **Python** and **SQLite** installed.
- Required packages (install via `pip`):
  ```bash
  pip install Flask SQLAlchemy sqlite3
  ```

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/username/INQUIRA.git
   ```
2. **Database Setup**:
   - Set up the SQLite database using the provided schema file.
   - Configure database paths in the backend code as needed.

3. **Run the Application**:
   ```bash
   python main.py
   ```

### Frontend Development
If using React for the frontend:
   ```bash
   cd frontend
   npm install
   npm start
   ```

### Usage
1. **Register** as a new user and create a profile.
2. **Search** for collaborators based on filters such as skills and location.
3. **Send Connection Requests** with personalized messages.
4. **Manage Connections** in the dashboard and toggle between light/dark mode.

## Future Enhancements
- **Automated Skill Assessment** via AI
- **In-App Messaging** for smoother communication
- **Enhanced Security and Privacy** settings
- **Mobile Application** for on-the-go networking


