from flask import Blueprint, render_template, redirect
from flask_login import login_required
from . import db
from .models import User 

dt = Blueprint('dt', __name__)

@dt.route('/dt/admin/<email>/10051998') 
@login_required
def dt_access(email):
	admin = User.query.filter_by(email=email).first_or_404()
	if admin:
		users=User.query.all()
		return render_template('/dt/dt.html', users=users)

	return redirect('main.index')