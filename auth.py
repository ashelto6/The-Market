from flask import Blueprint, render_template, redirect, url_for, request, flash
from password_strength import PasswordPolicy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from .check import ef5count, ef3count
from datetime import date
from . import db

auth = Blueprint('auth', __name__)

#login page route - GET
@auth.route('/login')
def login():
  if current_user:
    logout_user()
  today = date.today()
  today=today.strftime("%m/%d/%Y")
  return render_template('/auth/login.html', date=today)

#login page route - POST
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

#signup page route - GET
@auth.route('/signup')
def signup():
  today = date.today()
  today=today.strftime("%m/%d/%Y")
  return render_template('/auth/signup.html', date=today)

#signup page route - POST
@auth.route('/signup', methods = ['POST'])
def signup_post():
  first_name= request.form.get('first name')
  last_name = request.form.get('last name')
  email = request.form.get('email').lower()
  password = request.form.get('password')
  repassword = request.form.get('repassword')

  empty_fields = ef5count(first_name, last_name, email, password, repassword) #returns number of empty fields
  if empty_fields > 0:
    flash("Please enter a value for each field.")
    return redirect(url_for('auth.signup'))

  policy = PasswordPolicy.from_names(strength=0.30)
  err = policy.test(password)
  if len(err) > 0:
    flash('Password is not strong enough.')        
    return redirect(url_for('auth.signup'))
  
  if password != repassword:
    flash("Passwords do not match.")
    return redirect(url_for('auth.signup'))

  user = User.query.filter_by(email=email).first()
  if user:
    flash('Email address already exists.')
    return redirect(url_for('auth.signup'))

  new_user = User(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password, method='sha256'))
  db.session.add(new_user)
  db.session.commit()

  flash("Account Successfully Created!")
  return redirect(url_for('auth.login'))

#on logout button press - POST
@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('main.index'))

#settings subroute "change_password" - POST & GET
@auth.route('/settings/change_password', methods=['POST', 'GET'])
@login_required
def change_password():
  if request.method == 'GET':
    return redirect(url_for('main.settings'))
  
  old_password = request.form.get('Old password')
  new_password = request.form.get('New password')
  new_password_again = request.form.get('New password again')
  
  empty_fields = ef3count(old_password, new_password, new_password_again)
  if empty_fields > 0:
    flash('Please enter a value for each password field.')
    return redirect(url_for('main.settings'))
  
  if not check_password_hash(current_user.password, old_password):
    flash('The current password you entered is incorrect.')
    return redirect(url_for('main.settings'))
  
  policy = PasswordPolicy.from_names(strength=0.30)
  err = policy.test(new_password)
  if len(err) > 0:
    flash('New password is not strong enough.')        
    return redirect(url_for('main.settings'))
  
  if new_password != new_password_again:
    flash("New passwords do not match.")
    return redirect(url_for('main.settings'))
  
  if old_password == new_password:
    flash('You entered the same password for your current password and your new password.')
    return redirect(url_for('main.settings'))
  
  current_user.password=generate_password_hash(new_password, method='sha256')
  db.session.commit()
  flash("Password has been successfully changed! Login with your new password.")
  return redirect(url_for('auth.login'))

#settings subroute "edit_profile" - POST & GET
@auth.route('/settings/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
  if request.method == 'GET':
    return redirect(url_for('main.settings'))

  first_name=request.form.get('first name')
  last_name = request.form.get('last name')
  email = request.form.get('email').lower()
  user = User.query.filter_by(email=email).first()

  if first_name == current_user.first_name and last_name == current_user.last_name and email == current_user.email:
    flash('No changes were found.')
    return redirect(url_for('main.settings'))

  if email != current_user.email and user:
    flash('That email is taken.')
    return redirect(url_for('main.settings'))

  empty_fields = ef3count(first_name, last_name, email)
  if empty_fields > 0:
    flash('Please enter a value for each field.')
    return redirect(url_for('main.settings'))

  current_user.first_name = first_name
  current_user.last_name = last_name
  current_user.email = email
  db.session.commit()

  flash('Account Successfully Updated!')
  return redirect(url_for('main.settings'))

#settings subroute "delete account" - POST & GET
@auth.route('/settings/delete_account', methods=['POST', 'GET'])
@login_required
def delete_account():
  if request.method == 'GET':
    return redirect(url_for('main.settings'))
  
  if current_user:
    db.session.delete(current_user)
    db.session.commit()
  flash("Your account has been permanently deleted.")
  return redirect(url_for('main.index'))