from flask import Blueprint, render_template, redirect, jsonify, request, url_for,flash
from flask_login import login_required, current_user
from . import db, TDSession
from .models import User
from .check import ef3count
from dotenv import load_dotenv
import os, json, requests

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
main = Blueprint('main', __name__)

#homepage route
@main.route('/')
@main.route('/home')
def index():
	TDSession.login()
	#for large cap data ###############################################
	LCticklist=['TSLA','AMZN'] #ticker list 
	endpoint = "https://api.tdameritrade.com/v1/marketdata/quotes"
	payload = {'apikey':os.environ.get('CLIENT_ID'), 'symbol':LCticklist}
	content = requests.get(url=endpoint, params=payload)
	LCdata = content.json()
	###################################################################

	#for mid cap data #################################################
	MCticklist=['RIOT','JMIA'] #ticker list 
	endpoint = "https://api.tdameritrade.com/v1/marketdata/quotes"
	payload = {'apikey':os.environ.get('CLIENT_ID'), 'symbol':MCticklist}
	content = requests.get(url=endpoint, params=payload)
	MCdata = content.json()
	###################################################################
	
		#for penny cap data ##############################################
	PSticklist=['CTRM','ZOM'] #ticker list 
	endpoint = "https://api.tdameritrade.com/v1/marketdata/quotes"
	payload = {'apikey':os.environ.get('CLIENT_ID'), 'symbol':PSticklist}
	content = requests.get(url=endpoint, params=payload)
	PSdata = content.json()
	###################################################################
	return render_template("/main/index.html",  LCdata=LCdata, MCdata=MCdata, PSdata=PSdata)

#portfolio page route
@main.route('/portfolio')
@login_required
def portfolio():
	TDSession.login()
	data = TDSession.get_accounts(account='all', fields=['positions'])
	return render_template('/main/portfolio.html', name=current_user.first_name, data=data)

#settings pages route
@main.route('/settings')
@login_required
def settings():
 user=User.query.filter_by(email = current_user.email).first()
 
 return render_template('/main/settings.html', current_user=user)

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