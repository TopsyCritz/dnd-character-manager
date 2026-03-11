# D&D Character Manager

A web-based application for creating and managing Dungeons & Dragons characters.

## Features

- User registration and login with email/password
- Create characters with core D&D statistics (STR, DEX, CON, INT, WIS, CHA)
- View, edit, and delete characters
- Secure password hashing
- SQLite database for persistent storage

## Requirements

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Werkzeug

## Installation

1. Clone the repository or navigate to the project directory.

2. Install the required dependencies:
   ```
   pip install flask flask-sqlalchemy
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your browser and navigate to `http://127.0.0.1:5000`

## Usage

1. **Register**: Click "Register" to create a new account with your email and password.

2. **Login**: After registering, log in with your credentials.

3. **Create Character**: Click "New Character" to create a character with:
   - Character name
   - Strength (1-30)
   - Dexterity (1-30)
   - Constitution (1-30)
   - Intelligence (1-30)
   - Wisdom (1-30)
   - Charisma (1-30)

4. **Manage Characters**: View, edit, or delete your characters from the dashboard.

## Database

The database (`dnd characters.db`) is automatically created when you first run the application. It stores:
- User accounts (email and hashed passwords)
- Character data (linked to users)

## Project Structure

```
dnd-character-manager/
├── app.py                 # Main Flask application
├── static/
│   └── style.css         # Stylesheet
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── login.html        # Login form
│   ├── register.html     # Registration form
│   ├── dashboard.html    # User dashboard
│   ├── new_character.html # Character creation form
│   ├── view_character.html # Character details
│   └── edit_character.html # Character edit form
├── README.md             # This file
└── venv/                 # Virtual environment (if used)
```

## Security Notes

- Passwords are hashed using Werkzeug's security functions
- Session-based authentication
- Characters are tied to user accounts and can only be viewed/edited by the owner

## License

This project is for educational purposes.
