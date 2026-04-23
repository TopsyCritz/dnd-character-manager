from flask import Blueprint, render_template, request, redirect, url_for, session, flash, Response
from models import db, User, Character, SkillProficiency, SKILL_LIST
import json

routes = Blueprint('routes', __name__)


def build_character_data(character):
    """Build character data dictionary for display and export."""
    proficiency_bonus = character.get_proficiency_bonus()
    
    abilities = {
        'strength': {'value': character.strength, 'modifier': character.get_modifier('strength'), 'name': 'Strength'},
        'dexterity': {'value': character.dexterity, 'modifier': character.get_modifier('dexterity'), 'name': 'Dexterity'},
        'constitution': {'value': character.constitution, 'modifier': character.get_modifier('constitution'), 'name': 'Constitution'},
        'intelligence': {'value': character.intelligence, 'modifier': character.get_modifier('intelligence'), 'name': 'Intelligence'},
        'wisdom': {'value': character.wisdom, 'modifier': character.get_modifier('wisdom'), 'name': 'Wisdom'},
        'charisma': {'value': character.charisma, 'modifier': character.get_modifier('charisma'), 'name': 'Charisma'},
    }
    
    skills = []
    for skill_name, ability in SKILL_LIST:
        skill_mod = character.get_skill_modifier(skill_name)
        is_proficient = skill_name in character.get_proficient_skills()
        skills.append({
            'name': skill_name,
            'ability': ability,
            'ability_short': ability[:3].upper(),
            'modifier': skill_mod,
            'proficient': is_proficient
        })
    
    return {
        'proficiency_bonus': proficiency_bonus,
        'abilities': abilities,
        'skills': skills
    }


def character_to_dict(character):
    """Convert character to dictionary for JSON export."""
    data = build_character_data(character)
    
    return {
        'id': character.id,
        'name': character.name,
        'level': character.level,
        'proficiency_bonus': data['proficiency_bonus'],
        'abilities': data['abilities'],
        'skills': data['skills']
    }


@routes.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('routes.dashboard'))
    return render_template('index.html')


@routes.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('routes.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return render_template('register.html')
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.', 'error')
            return render_template('register.html')
        
        new_user = User(email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('routes.login'))
    
    return render_template('register.html')


@routes.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('routes.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['email'] = user.email
            return redirect(url_for('routes.dashboard'))
        
        flash('Invalid email or password.', 'error')
        return render_template('login.html')
    
    return render_template('login.html')


@routes.route('/toggle-theme')
def toggle_theme():
    current_theme = session.get('theme', 'light')
    session['theme'] = 'dark' if current_theme == 'light' else 'light'
    return redirect(request.referrer or url_for('routes.index'))


@routes.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('email', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('routes.login'))


@routes.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    
    user = User.query.get(session['user_id'])
    characters = Character.query.filter_by(user_id=session['user_id']).all()
    
    for character in characters:
        character.proficiency_bonus = character.get_proficiency_bonus()
        character.str_mod = character.get_modifier('strength')
        character.dex_mod = character.get_modifier('dexterity')
        character.con_mod = character.get_modifier('constitution')
        character.int_mod = character.get_modifier('intelligence')
        character.wis_mod = character.get_modifier('wisdom')
        character.cha_mod = character.get_modifier('charisma')
        character.proficient_skills = character.get_proficient_skills()
    
    return render_template('dashboard.html', user=user, characters=characters)


@routes.route('/character/new', methods=['GET', 'POST'])
def new_character():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        
        try:
            level = int(request.form.get('level', 1))
            strength = int(request.form.get('strength', 0))
            dexterity = int(request.form.get('dexterity', 0))
            constitution = int(request.form.get('constitution', 0))
            intelligence = int(request.form.get('intelligence', 0))
            wisdom = int(request.form.get('wisdom', 0))
            charisma = int(request.form.get('charisma', 0))
        except ValueError:
            flash('All stats must be numeric values.', 'error')
            return render_template('new_character.html', skill_list=SKILL_LIST)
        
        if not name:
            flash('Character name is required.', 'error')
            return render_template('new_character.html', skill_list=SKILL_LIST)
        
        if not (1 <= level <= 20):
            flash('Level must be between 1 and 20.', 'error')
            return render_template('new_character.html', skill_list=SKILL_LIST)
        
        if not all(1 <= stat <= 30 for stat in [strength, dexterity, constitution, intelligence, wisdom, charisma]):
            flash('Stats must be between 1 and 30.', 'error')
            return render_template('new_character.html', skill_list=SKILL_LIST)
        
        character = Character(
            name=name,
            level=level,
            strength=strength,
            dexterity=dexterity,
            constitution=constitution,
            intelligence=intelligence,
            wisdom=wisdom,
            charisma=charisma,
            user_id=session['user_id']
        )
        db.session.add(character)
        db.session.commit()
        
        for skill_name, _ in SKILL_LIST:
            if f'skill_{skill_name.lower().replace(" ", "_")}' in request.form:
                prof = SkillProficiency(character_id=character.id, skill_name=skill_name)
                db.session.add(prof)
        db.session.commit()
        
        flash('Character created successfully!', 'success')
        return redirect(url_for('routes.dashboard'))
    
    return render_template('new_character.html', skill_list=SKILL_LIST)


@routes.route('/character/<int:character_id>')
def view_character(character_id):
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    
    character = Character.query.get_or_404(character_id)
    
    if character.user_id != session['user_id']:
        flash('You do not have permission to view this character.', 'error')
        return redirect(url_for('routes.dashboard'))
    
    data = build_character_data(character)
    
    return render_template('view_character.html', 
                         character=character, 
                         proficiency_bonus=data['proficiency_bonus'], 
                         abilities=data['abilities'],
                         skills=data['skills'],
                         skill_list=SKILL_LIST)


@routes.route('/character/<int:character_id>/edit', methods=['GET', 'POST'])
def edit_character(character_id):
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    
    character = Character.query.get_or_404(character_id)
    
    if character.user_id != session['user_id']:
        flash('You do not have permission to edit this character.', 'error')
        return redirect(url_for('routes.dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        
        try:
            level = int(request.form.get('level', 1))
            strength = int(request.form.get('strength', 0))
            dexterity = int(request.form.get('dexterity', 0))
            constitution = int(request.form.get('constitution', 0))
            intelligence = int(request.form.get('intelligence', 0))
            wisdom = int(request.form.get('wisdom', 0))
            charisma = int(request.form.get('charisma', 0))
        except ValueError:
            flash('All stats must be numeric values.', 'error')
            return render_template('edit_character.html', character=character, skill_list=SKILL_LIST)
        
        if not name:
            flash('Character name is required.', 'error')
            return render_template('edit_character.html', character=character, skill_list=SKILL_LIST)
        
        if not (1 <= level <= 20):
            flash('Level must be between 1 and 20.', 'error')
            return render_template('edit_character.html', character=character, skill_list=SKILL_LIST)
        
        if not all(1 <= stat <= 30 for stat in [strength, dexterity, constitution, intelligence, wisdom, charisma]):
            flash('Stats must be between 1 and 30.', 'error')
            return render_template('edit_character.html', character=character, skill_list=SKILL_LIST)
        
        character.name = name
        character.level = level
        character.strength = strength
        character.dexterity = dexterity
        character.constitution = constitution
        character.intelligence = intelligence
        character.wisdom = wisdom
        character.charisma = charisma
        
        SkillProficiency.query.filter_by(character_id=character.id).delete()
        
        for skill_name, _ in SKILL_LIST:
            if f'skill_{skill_name.lower().replace(" ", "_")}' in request.form:
                prof = SkillProficiency(character_id=character.id, skill_name=skill_name)
                db.session.add(prof)
        
        db.session.commit()
        
        flash('Character updated successfully!', 'success')
        return redirect(url_for('routes.view_character', character_id=character.id))
    
    proficient_skills = character.get_proficient_skills()
    return render_template('edit_character.html', character=character, skill_list=SKILL_LIST, proficient_skills=proficient_skills)


@routes.route('/character/<int:character_id>/delete', methods=['POST'])
def delete_character(character_id):
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    
    character = Character.query.get_or_404(character_id)
    
    if character.user_id != session['user_id']:
        flash('You do not have permission to delete this character.', 'error')
        return redirect(url_for('routes.dashboard'))
    
    db.session.delete(character)
    db.session.commit()
    
    flash('Character deleted successfully!', 'success')
    return redirect(url_for('routes.dashboard'))


@routes.route('/export/json/<int:character_id>')
def export_json(character_id):
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    
    character = Character.query.get_or_404(character_id)
    
    if character.user_id != session['user_id']:
        flash('You do not have permission to export this character.', 'error')
        return redirect(url_for('routes.dashboard'))
    
    data = character_to_dict(character)
    
    return Response(
        json.dumps(data, indent=4),
        mimetype="application/json",
        headers={
            "Content-Disposition": f"attachment; filename=character_{character_id}.json"
        }
    )
