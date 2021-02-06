from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)

#homepage route
@main.route('/')
@main.route('/home')
def index():
	return render_template("/main/index.html")

#trades page route
@main.route('/portfolio')
@login_required
def portfolio():
	return render_template('/main/portfolio.html', name=current_user.first_name)
