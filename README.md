# D&D Character Manager

A Flask web application for creating, managing, and sharing Dungeons & Dragons 5th Edition characters.

## Features

### User Authentication
- Register, login, and logout with email and password
- Session-based authentication with secure password hashing
- Characters are private to each user account

### Character Management
- Create, view, edit, and delete characters
- Character level tracking (1–20)
- Hit Point system with manual max HP and current HP
- Visual HP bar with low HP indicator (turns red below 50%)

### Ability Scores
- Six core ability scores: STR, DEX, CON, INT, WIS, CHA
- Automatic ability modifier calculation: `floor((score - 10) / 2)`

### Skill System
- 18 official D&D 5e skills mapped to their governing abilities
- Proficiency checkboxes for each skill
- Automatic skill modifier calculation:
  - Proficient: `ability_modifier + proficiency_bonus`
  - Not proficient: `ability_modifier` only

### Proficiency Bonus
Calculated based on character level:
| Level | Bonus |
|-------|-------|
| 1–4   | +2    |
| 5–8   | +3    |
| 9–12  | +4    |
| 13–16 | +5    |
| 17–20 | +6    |

### Import / Export
- Export characters as downloadable JSON files
- Import characters from previously exported JSON files
- Imported characters use validated raw data with recalculated modifiers

### Interface
- Dark mode toggle (persists per session)
- Character dashboard showing overview of all characters
- Detailed character sheet with abilities, modifiers, skills, and HP

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd dnd-character-manager
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install flask flask-sqlalchemy
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open your browser to `http://127.0.0.1:5000`

## Usage

### Creating a Character
1. Log in and click "Create New Character" on the dashboard
2. Enter the character name and level (1–20)
3. Set Max HP and Current HP (current HP defaults to Max HP)
4. Enter ability scores (1–30 for each)
5. Select skill proficiencies by checking the appropriate boxes
6. Click "Create Character"

### Editing a Character
1. From the character view, click "Edit"
2. Modify any field: name, level, HP, ability scores, or skill proficiencies
3. Current HP must be between 0 and Max HP
4. Click "Save Changes"

### Skill Proficiency
When creating or editing a character, check the box next to each skill your character is proficient in. The application automatically:
- Calculates the ability modifier from the governing ability score
- Adds the proficiency bonus based on character level (if proficient)
- Displays the final skill modifier on the character sheet

### Managing Hit Points
HP is entered manually when creating or editing a character:
- Max HP represents the character's total hit point maximum
- Current HP represents the character's current health
- The HP bar on the character sheet turns red when current HP falls below 50% of max HP
- Edit a character at any time to adjust current HP after taking damage or healing

### Exporting a Character
1. Open the character's detail view
2. Click "Export JSON"
3. A file named `character_<id>.json` will download

### Importing a Character
1. From the dashboard, click "Import Character"
2. Select a previously exported JSON file
3. The application validates the file and creates a new character
4. Only raw data is imported (name, level, ability scores, skill proficiencies)
5. All modifiers are recalculated automatically
6. The new character appears on your dashboard

## Project Structure

| File/Directory       | Description |
|---------------------|-------------|
| `app.py`            | Flask application initialization and configuration |
| `models.py`         | Database models (User, Character, SkillProficiency) and D&D calculation methods |
| `routes.py`         | Route handlers, JSON export/import logic, helper functions |
| `templates/`        | HTML templates using Jinja2 |
| `static/style.css`  | Stylesheet with light and dark theme support |
| `instance/`         | SQLite database (auto-created on first run) |

## Database Schema

- **User**: id, email, password_hash
- **Character**: id, name, level, max_hp, current_hp, ability scores, user_id
- **SkillProficiency**: id, character_id, skill_name

The `Character` model includes methods for calculating modifiers, proficiency bonuses, and skill values. All calculations are performed server-side.

## Technologies

- **Python 3.8+**
- **Flask** – Web framework
- **Flask-SQLAlchemy** – ORM and database management
- **Werkzeug** – Password hashing utilities
- **SQLite** – Relational database
- **Jinja2** – Template engine
- **HTML/CSS** – Frontend with responsive design

## Future Improvements

- Character classes and automatic hit die calculation
- Constitution-based HP calculations
- Inventory and equipment management
- Spell tracking and spell slots
- Saving throws with proficiency
- Rest tracking (short rest, long rest)
- Character notes and background information
- UI polish and animations
