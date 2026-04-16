# D&D Character Manager

A web-based application for creating and managing Dungeons & Dragons 5th Edition characters.

## Features

- User registration and login with email/password
- Create characters with D&D 5e ability scores and level
- Full skill system with 18 skills and proficiency tracking
- Automatic calculation of ability modifiers and skill bonuses
- View, edit, and delete characters
- Dark mode toggle
- Secure password hashing
- SQLite database for persistent storage

## D&D 5e Rules Implemented

- **Ability Scores**: Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma
- **Ability Modifiers**: Calculated as `(score - 10) / 2`
- **Proficiency Bonus**: Based on character level
  - Levels 1-4: +2
  - Levels 5-8: +3
  - Levels 9-12: +4
  - Levels 13-16: +5
  - Levels 17-20: +6
- **Skills**: 18 skills mapped to abilities with proficiency checkboxes

### Skill List

| Ability | Skills |
|---------|--------|
| Strength | Athletics |
| Dexterity | Acrobatics, Sleight of Hand, Stealth |
| Intelligence | Arcana, History, Investigation, Nature, Religion |
| Wisdom | Animal Handling, Insight, Medicine, Perception, Survival |
| Charisma | Deception, Intimidation, Performance, Persuasion |

### Skill Check Formula
- `skill_modifier = ability_modifier + proficiency_bonus` (if proficient)
- `skill_modifier = ability_modifier` (if not proficient)

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
   - Character level (1-20)
   - Ability scores (1-30 each):
     - Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma
   - Skill proficiencies (select any skills your character is proficient in)

4. **View Character**: See your character's ability scores with modifiers and all skills with calculated bonuses.

5. **Manage Characters**: View, edit, or delete your characters from the dashboard.

6. **Dark Mode**: Toggle dark/light theme using the moon/sun icon in the navigation bar.

## Database

The database (`instance/dnd characters.db`) is automatically created when you first run the application. It stores:
- User accounts (email and hashed passwords)
- Character data with ability scores and level
- Skill proficiencies (linked to characters)

## Project Structure

```
dnd-character-manager/
├── app.py                 # Flask application initialization
├── models.py              # Database models and D&D logic
├── routes.py              # Route handlers
├── static/
│   └── style.css         # Stylesheet
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── login.html        # Login form
│   ├── register.html     # Registration form
│   ├── dashboard.html    # User dashboard
│   ├── new_character.html # Character creation form
│   ├── view_character.html # Character sheet view
│   └── edit_character.html # Character edit form
├── instance/             # Database folder (auto-created)
├── README.md             # This file
└── venv/                 # Virtual environment (if used)
```

## Security Notes

- Passwords are hashed using Werkzeug's security functions
- Session-based authentication
- Characters are tied to user accounts and can only be viewed/edited by the owner

## License

This project is for educational purposes.
