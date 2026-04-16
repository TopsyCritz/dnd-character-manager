from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import math

db = SQLAlchemy()


SKILLS = {
    'Acrobatics': 'dexterity',
    'Animal Handling': 'wisdom',
    'Arcana': 'intelligence',
    'Athletics': 'strength',
    'Deception': 'charisma',
    'History': 'intelligence',
    'Insight': 'wisdom',
    'Intimidation': 'charisma',
    'Investigation': 'intelligence',
    'Medicine': 'wisdom',
    'Nature': 'intelligence',
    'Perception': 'wisdom',
    'Performance': 'charisma',
    'Persuasion': 'charisma',
    'Religion': 'intelligence',
    'Sleight of Hand': 'dexterity',
    'Stealth': 'dexterity',
    'Survival': 'wisdom',
}

SKILL_LIST = [
    ('Athletics', 'strength'),
    ('Acrobatics', 'dexterity'),
    ('Sleight of Hand', 'dexterity'),
    ('Stealth', 'dexterity'),
    ('Arcana', 'intelligence'),
    ('History', 'intelligence'),
    ('Investigation', 'intelligence'),
    ('Nature', 'intelligence'),
    ('Religion', 'intelligence'),
    ('Animal Handling', 'wisdom'),
    ('Insight', 'wisdom'),
    ('Medicine', 'wisdom'),
    ('Perception', 'wisdom'),
    ('Survival', 'wisdom'),
    ('Deception', 'charisma'),
    ('Intimidation', 'charisma'),
    ('Performance', 'charisma'),
    ('Persuasion', 'charisma'),
]


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    characters = db.relationship('Character', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, nullable=False, default=1)
    strength = db.Column(db.Integer, nullable=False)
    dexterity = db.Column(db.Integer, nullable=False)
    constitution = db.Column(db.Integer, nullable=False)
    intelligence = db.Column(db.Integer, nullable=False)
    wisdom = db.Column(db.Integer, nullable=False)
    charisma = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    skill_proficiencies = db.relationship('SkillProficiency', backref='character', lazy=True, cascade='all, delete-orphan')

    def get_modifier(self, ability):
        score = getattr(self, ability)
        return (score - 10) // 2

    def get_proficiency_bonus(self):
        level = self.level
        if level < 5:
            return 2
        elif level < 9:
            return 3
        elif level < 13:
            return 4
        elif level < 17:
            return 5
        else:
            return 6

    def get_skill_modifier(self, skill_name):
        ability = SKILLS[skill_name]
        ability_mod = self.get_modifier(ability)
        prof_bonus = self.get_proficiency_bonus()
        
        is_proficient = SkillProficiency.query.filter_by(
            character_id=self.id,
            skill_name=skill_name
        ).first() is not None
        
        if is_proficient:
            return ability_mod + prof_bonus
        return ability_mod

    def get_proficient_skills(self):
        proficiencies = SkillProficiency.query.filter_by(character_id=self.id).all()
        return {p.skill_name for p in proficiencies}


class SkillProficiency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    skill_name = db.Column(db.String(50), nullable=False)
