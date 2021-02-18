from flask import Blueprint, render_template, redirect,jsonify
from flask_login import login_required, current_user
from . import db, TDSession
from .models import User
from dotenv import load_dotenv
import os, json, requests, collections

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
main = Blueprint('main', __name__)

#homepage route
@main.route('/')
@main.route('/home')
def index():
	TDSession.login()

	#for large cap data ###############################################
	LCticklist=['GOOG','MSFT'] #ticker list 
	endpoint = "https://api.tdameritrade.com/v1/marketdata/quotes"
	payload = {'apikey':os.environ.get('CLIENT_ID'), 'symbol':LCticklist}
	content = requests.get(url=endpoint, params=payload)
	LCdata = content.json()
	###################################################################

	#for mid cap data #################################################
	MCticklist=['CROX','PLUG'] #ticker list 
	endpoint = "https://api.tdameritrade.com/v1/marketdata/quotes"
	payload = {'apikey':os.environ.get('CLIENT_ID'), 'symbol':MCticklist}
	content = requests.get(url=endpoint, params=payload)
	MCdata = content.json()
	###################################################################
	
		#for penny cap data ##############################################
	PSticklist=['AEZS','ZOM'] #ticker list 
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