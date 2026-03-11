from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dnd characters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    characters = db.relationship('Character', backref='owner', lazy=True)


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    strength = db.Column(db.Integer, nullable=False)
    dexterity = db.Column(db.Integer, nullable=False)
    constitution = db.Column(db.Integer, nullable=False)
    intelligence = db.Column(db.Integer, nullable=False)
    wisdom = db.Column(db.Integer, nullable=False)
    charisma = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
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
        
        new_user = User(
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['email'] = user.email
            return redirect(url_for('dashboard'))
        
        flash('Invalid email or password.', 'error')
        return render_template('login.html')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('email', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    characters = Character.query.filter_by(user_id=session['user_id']).all()
    return render_template('dashboard.html', user=user, characters=characters)


@app.route('/character/new', methods=['GET', 'POST'])
def new_character():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        
        try:
            strength = int(request.form.get('strength', 0))
            dexterity = int(request.form.get('dexterity', 0))
            constitution = int(request.form.get('constitution', 0))
            intelligence = int(request.form.get('intelligence', 0))
            wisdom = int(request.form.get('wisdom', 0))
            charisma = int(request.form.get('charisma', 0))
        except ValueError:
            flash('All stats must be numeric values.', 'error')
            return render_template('new_character.html')
        
        if not name:
            flash('Character name is required.', 'error')
            return render_template('new_character.html')
        
        if not all(1 <= stat <= 30 for stat in [strength, dexterity, constitution, intelligence, wisdom, charisma]):
            flash('Stats must be between 1 and 30.', 'error')
            return render_template('new_character.html')
        
        character = Character(
            name=name,
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
        
        flash('Character created successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('new_character.html')


@app.route('/character/<int:character_id>')
def view_character(character_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    character = Character.query.get_or_404(character_id)
    
    if character.user_id != session['user_id']:
        flash('You do not have permission to view this character.', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('view_character.html', character=character)


@app.route('/character/<int:character_id>/edit', methods=['GET', 'POST'])
def edit_character(character_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    character = Character.query.get_or_404(character_id)
    
    if character.user_id != session['user_id']:
        flash('You do not have permission to edit this character.', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        
        try:
            strength = int(request.form.get('strength', 0))
            dexterity = int(request.form.get('dexterity', 0))
            constitution = int(request.form.get('constitution', 0))
            intelligence = int(request.form.get('intelligence', 0))
            wisdom = int(request.form.get('wisdom', 0))
            charisma = int(request.form.get('charisma', 0))
        except ValueError:
            flash('All stats must be numeric values.', 'error')
            return render_template('edit_character.html', character=character)
        
        if not name:
            flash('Character name is required.', 'error')
            return render_template('edit_character.html', character=character)
        
        if not all(1 <= stat <= 30 for stat in [strength, dexterity, constitution, intelligence, wisdom, charisma]):
            flash('Stats must be between 1 and 30.', 'error')
            return render_template('edit_character.html', character=character)
        
        character.name = name
        character.strength = strength
        character.dexterity = dexterity
        character.constitution = constitution
        character.intelligence = intelligence
        character.wisdom = wisdom
        character.charisma = charisma
        
        db.session.commit()
        
        flash('Character updated successfully!', 'success')
        return redirect(url_for('view_character', character_id=character.id))
    
    return render_template('edit_character.html', character=character)


@app.route('/character/<int:character_id>/delete', methods=['POST'])
def delete_character(character_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    character = Character.query.get_or_404(character_id)
    
    if character.user_id != session['user_id']:
        flash('You do not have permission to delete this character.', 'error')
        return redirect(url_for('dashboard'))
    
    db.session.delete(character)
    db.session.commit()
    
    flash('Character deleted successfully!', 'success')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
