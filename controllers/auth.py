from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
from models.user import User, db

auth_bp = Blueprint('auth', __name__)

mail = Mail()


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Email already exists!')
            return redirect(url_for('auth.register'))
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        send_confirmation_email(email)

        return redirect(url_for('auth.login'))
    return render_template('register.html')


def send_confirmation_email(email):
    msg = Message("Welcome to Our App", recipients=[email])
    msg.body = "Thank you for registering!"
    mail.send(msg)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['email'] = email
            return redirect(url_for('auth.home'))
        flash('Invalid email or password!')
    return render_template('login.html')


@auth_bp.route('/home')
def home():
    if 'email' not in session:
        return redirect(url_for('auth.login'))
    return render_template('home.html')


@auth_bp.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('auth.login'))
