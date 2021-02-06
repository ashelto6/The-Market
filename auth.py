from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
 return render_template('/auth/login.html')

@auth.route('/signup')
def signup():
 return render_template('/auth/signup.html')

@auth.route('/signup', methods = ['POST'])
def signup_post():
 first_name= request.form.get('first name')
 last_name = request.form.get('last name')
 email = request.form.get('email')
 password = request.form.get('password')

 user = User.query.filter_by(email=email).first()
 
 if user:
  flash('Email address already exists')
  return redirect(url_for('auth.signup'))

 new_user = User(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password, method='sha256'))

 db.session.add(new_user)
 db.session.commit()

 return redirct(url_for('auth.login'))

@auth.route('/logout')
def logout():
 return render_template('/auth/logout.html')