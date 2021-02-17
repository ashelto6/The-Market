from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from .check import efcount
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
  if current_user:
    logout_user()
  return render_template('/auth/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
  email = request.form.get('email').lower()
  password = request.form.get('password')
  remember = True if request.form.get('remember') else False

  user = User.query.filter_by(email=email).first()

  if not user or not check_password_hash(user.password, password):
    flash('Please check your login credentials and try again.')
    return redirect(url_for('auth.login'))

  login_user(user, remember=remember)
  flash(f'Login Successful, Welcome {current_user.first_name}!')
  return redirect(url_for('main.portfolio'))

@auth.route('/signup')
def signup():
  return render_template('/auth/signup.html')

@auth.route('/signup', methods = ['POST'])
def signup_post():
  first_name= request.form.get('first name')
  last_name = request.form.get('last name')
  email = request.form.get('email').lower()
  password = request.form.get('password')
  repassword = request.form.get('repassword')

  empty_fields = efcount(first_name, last_name, email, password, repassword) #returns number of empty fields
  if empty_fields > 0:
    flash("Please enter a value for each field.")
    return redirect(url_for('auth.signup'))

  if password != repassword:
    flash("Passwords do not match, Please try again.")
    return redirect(url_for('auth.signup'))

  user = User.query.filter_by(email=email).first()
  if user:
    flash('Email address already exists')
    return redirect(url_for('auth.signup'))

  new_user = User(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password, method='sha256'))
  db.session.add(new_user)
  db.session.commit()

  flash("Account Successfully Created!")
  return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('main.index'))