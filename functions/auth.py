from flask import app, flash, url_for
from flask_login import login_user
from flask_mail import Message
from app import mail, mongo
from itsdangerous import URLSafeTimedSerializer
from app import app
from models import User

s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

def handle_password_reset(email):
    user = mongo.db.users.find_one({"email": email})
    if user:
        token = s.dumps(email, salt='password-reset-salt')
        msg = Message('Password Reset Request', sender='your-email@gmail.com', recipients=[email])
        link = url_for('auth.reset_token', token=token, _external=True)
        msg.body = f'Your link is {link}'
        mail.send(msg)
        flash('An email has been sent with instructions to reset your password.')
        return True
    else:
        flash('Email not found.')
        return False
    
def handle_login(username, password):
    user_data = mongo.db.users.find_one({"username": username})
    if user_data and user_data['password'] == password:
        user = User(user_data['_id'], user_data['username'])
        login_user(user)
        return True
    return False

def handle_registration(username, password, email, first_name, last_name):
    existing_user = mongo.db.users.find_one({"$or": [{"username": username}, {"email": email}]})
    if existing_user:
        if existing_user['username'] == username:
            flash('Username already exists')
        else:
            flash('Email already exists')
        return False
    else:
        new_user = {
            "username": username,
            "password": password,
            "email": email,
            "first_name": first_name,
            "last_name": last_name
        }
        mongo.db.users.insert_one(new_user)
        flash('Registration successful')
        return True
    
def password_reset(email, new_password, confirm_password):
    if new_password != confirm_password:
        flash('Passwords do not match.')
        return False
    
    mongo.db.users.update_one({"email": email}, {"$set": {"password": new_password}})
    flash('Your password has been updated!')
    return True