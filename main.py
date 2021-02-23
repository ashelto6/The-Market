from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from . import db, TDSession
from .models import User
from .check import ef3count
from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
main = Blueprint('main', __name__)

#homepage route - GET
@main.route('/')
@main.route('/home')
def index():
	TDSession.login()
	#for large cap data 
	LCticklist=['GOOG','TSLA','AMZN'] #ticker list
	LCdata = TDSession.get_quotes(instruments=LCticklist)
	LCdata_list=[]
	for tick in LCticklist:
		LCdata_list.append(LCdata[tick])
	LCdata=LCdata_list

	#for mid cap data
	MCticklist=['PLUG','RIOT','JMIA'] #ticker list 
	MCdata = TDSession.get_quotes(instruments=MCticklist)
	MCdata_list=[]
	for tick in MCticklist:
		MCdata_list.append(MCdata[tick])
	MCdata=MCdata_list
	
	#for penny cap data
	PSticklist=['AEZS','CTRM','ZOM'] #ticker list 
	PSdata = TDSession.get_quotes(instruments=PSticklist)
	PSdata_list=[]
	for tick in PSticklist:
		PSdata_list.append(PSdata[tick])
	PSdata=PSdata_list
 
	return render_template("/main/index.html",  LCdata=LCdata, MCdata=MCdata, PSdata=PSdata)

#portfolio page route - GET
@main.route('/portfolio')
@login_required
def portfolio():
	TDSession.login()
	data = TDSession.get_accounts(account='all', fields=['positions'])
	return render_template('/main/portfolio.html', name=current_user.first_name, data=data)

#settings pages route - GET
@main.route('/settings')
@login_required
def settings():
 user=User.query.filter_by(email = current_user.email).first()
 return render_template('/main/settings.html', current_user=user)

#settings subroute "edit_profile" - POST & GET
@main.route('/settings/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
 
 if request.method == 'GET':
  return redirect(url_for('main.settings'))
 
 first_name=request.form.get('first name')
 last_name = request.form.get('last name')
 email = request.form.get('email').lower()
 user = User.query.filter_by(email=email).first()
 
 if first_name == current_user.first_name and last_name == current_user.last_name and email == current_user.email:
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