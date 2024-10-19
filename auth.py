from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, logout_user
from functions.auth import handle_login, handle_password_reset, handle_registration, password_reset
from itsdangerous import URLSafeTimedSerializer
from app import app

auth = Blueprint('auth', __name__)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if handle_login(username, password):
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password')
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')        
        if handle_registration(username, password, email, first_name, last_name):
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        handle_password_reset(email)
    return render_template('auth/reset_password.html')

@auth.route('/reset_token/<token>', methods=['GET', 'POST'])
def reset_token(token):
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.')
        return redirect(url_for('auth.reset_password'))
    if request.method == 'POST':
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password') 
        if password_reset(email, new_password, confirm_password):
            return redirect(url_for('auth.login'))  
    return render_template('auth/reset_token.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))