from flask import Blueprint, render_template
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
 return render_template('/auth/login.html')

@auth.route('/signup')
def signup():
 return render_template('/auth/signup.html')

@auth.route('/logout')
def logout():
 return render_template('/auth/logout.html')