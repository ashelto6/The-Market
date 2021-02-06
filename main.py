from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from . import db
from .models import User

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

@main.route('/dt/admin/<email>/10051998') #put in separate file & .gitignore
@login_required
def dt(email):
	admin = User.query.filter_by(email=email).first_or_404()
	if admin:
		users=User.query.all()
		return render_template('/dt/dt.html', users=users)

	return redirect('main.index')

#ADD CONTENT TO THE HOMEPAGE, AND WORK ON GETTING TDAMERITRADE DATA DISPLAYED ON THE PORTFOLIO PAGE