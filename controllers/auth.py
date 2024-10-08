from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
from models.user import User, db
import random
import string

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

        confirmation_code = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        user = User(email=email)
        user.set_password(password)
        user.confirmation_code = confirmation_code
        db.session.add(user)
        db.session.commit()

        send_confirmation_email(email, confirmation_code)

        flash('Registration successful! Please check your email to confirm.')
        return redirect(url_for('auth.login'))
    return render_template('register.html')


def send_confirmation_email(email, confirmation_code):
    confirmation_url = url_for('auth.confirm_email', code=confirmation_code, _external=True)
    msg = Message("Confirm Your Registration", recipients=[email])
    msg.body = f"Thank you for registering! Please confirm your registration by clicking the following link: {confirmation_url}"
    mail.send(msg)


@auth_bp.route('/confirm/<code>')
def confirm_email(code):
    user = User.query.filter_by(confirmation_code=code).first()
    if user:
        user.confirmed = True
        user.confirmation_code = None
        db.session.commit()
        flash('Your email has been confirmed! You can now log in.')
        return redirect(url_for('auth.login'))
    flash('Invalid confirmation code!')
    return redirect(url_for('auth.register'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            if not user.confirmed:
                flash('Please confirm your email before logging in.')
                return redirect(url_for('auth.login'))
            session['email'] = email
            return redirect(url_for('auth.home'))
        flash('Invalid email or password!')
    return render_template('login.html')


@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            reset_code = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            user.confirmation_code = reset_code
            db.session.commit()
            send_password_reset_email(email, reset_code)
            flash('Password reset email sent!')
        else:
            flash('Email not found!')
        return redirect(url_for('auth.login'))
    return render_template('forgot_password.html')


def send_password_reset_email(email, reset_code):
    reset_url = url_for('auth.reset_password', code=reset_code, _external=True)
    msg = Message("Reset Your Password", recipients=[email])
    msg.body = f"Please reset your password by clicking the following link: {reset_url}"
    mail.send(msg)


@auth_bp.route('/reset_password/<code>', methods=['GET', 'POST'])
def reset_password(code):
    user = User.query.filter_by(confirmation_code=code).first()
    if not user:
        flash('Invalid or expired reset code!')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        new_password = request.form['password']
        user.set_password(new_password)
        user.confirmation_code = None
        db.session.commit()
        flash('Your password has been reset! You can now log in.')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html')


@auth_bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'email' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        user = User.query.filter_by(email=session['email']).first()

        if user and user.check_password(current_password):
            user.set_password(new_password)
            db.session.commit()
            flash('Your password has been changed successfully!')
            return redirect(url_for('auth.home'))
        else:
            flash('Current password is incorrect!')

    return render_template('change_password.html')


@auth_bp.route('/home')
def home():
    if 'email' not in session:
        return redirect(url_for('auth.login'))
    return render_template('home.html')


@auth_bp.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('auth.login'))
