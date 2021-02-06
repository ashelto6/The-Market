from flask import Blueprint, render_template
from . import db

main = Blueprint('main', __name__)

#homepage route
@main.route('/')
@main.route('/home')
def hello():
	return render_template("/main/index.html")

#trades page route
@main.route('/portfolio')
def trades():
	return render_template("/main/portfolio.html")
