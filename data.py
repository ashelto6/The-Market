from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from . import db
from .models import User

data = Blueprint('data', __name__)

@data.route('/data/admin/<email>/10051998')
@login_required
def data(email):
	admin = User.query.filter_by(email=email).first_or_404()
	if admin:
		users=User.query.all()
		return render_template('/data/data.html', users=users)

	return redirect('main.index')