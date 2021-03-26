from flask import Blueprint, render_template, redirect, request, url_for, flash, jsonify
from flask_login import login_required, current_user
from . import db, TDSession
from .models import User
from dotenv import load_dotenv
from datetime import date
import os
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
main = Blueprint('main', __name__)

#homepage route - GET
@main.route('/')
@main.route('/home')
def index():
	TDSession.login()
	my_file = open("symbols/bluechip.txt")
	content = my_file.read()
	BCticklist = content.split(", ")
	my_file.close()
	BCdata = TDSession.get_quotes(instruments=BCticklist)
	BCdata_list=[]
	for tick in BCticklist:
		BCdata_list.append(BCdata[tick])
	BCdata=BCdata_list

	my_file = open("symbols/smallcap.txt")
	content = my_file.read()
	SCticklist = content.split(", ")
	my_file.close()
	SCdata = TDSession.get_quotes(instruments=SCticklist)
	SCdata_list=[]
	for tick in SCticklist:
		SCdata_list.append(SCdata[tick])
	SCdata=SCdata_list
	
	my_file = open("symbols/featured.txt")
	content = my_file.read()
	Fticklist = content.split(", ")
	my_file.close()
	Fdata = TDSession.get_quotes(instruments=Fticklist)
	Fdata_list=[]
	for tick in Fticklist:
		Fdata_list.append(Fdata[tick])
	Fdata=Fdata_list
 
	today = date.today()
	today=today.strftime("%m/%d/%Y")
 
	return render_template("/main/index.html",  BCdata=BCdata, SCdata=SCdata, Fdata=Fdata, date=today)

#portfolio page route - GET
@main.route('/portfolio')
@login_required
def portfolio():
	TDSession.login()
	data = TDSession.get_accounts(account='all', fields=['positions'])
	today = date.today()
	today=today.strftime("%m/%d/%Y")
	return render_template('/main/portfolio.html', name=current_user.first_name, data=data, date=today)
 
#watchlist page route - GET
@main.route('/watchlist')
def watchlist():
	TDSession.login()
	data = TDSession.get_watchlist(account=os.environ.get('TD'), watchlist_id=os.environ.get('TDWL'))
	WLTickers = []
	for ticker in data['watchlistItems']:
		WLTickers.append(ticker['instrument']['symbol'])
	WLdata = TDSession.get_quotes(instruments=WLTickers)
 
	WLdata_list=[]
	for tick in WLTickers:
		WLdata_list.append(WLdata[tick])
	WLdata=WLdata_list
 
	today = date.today()
	today=today.strftime("%m/%d/%Y")
	return render_template('/main/watchlist.html', WLdata=WLdata, date=today)

#settings pages route - GET
@main.route('/settings')
@login_required
def settings():
 user=User.query.filter_by(email = current_user.email).first()
 today = date.today()
 today = today.strftime("%m/%d/%Y") 
 return render_template('/main/settings.html', current_user=user, date=today)

######################################### AJAX ROUTES ##############################################

#PSData AJAX route - POST
@main.route('/update_Fdata', methods=['POST'])
def updateFdata():
	TDSession.login()
	my_file = open("symbols/featured.txt")
	content = my_file.read()
	Fticklist = content.split(", ")
	my_file.close()
	Fdata = TDSession.get_quotes(instruments=Fticklist)
	Fdata_list=[]
	for tick in Fticklist:
		Fdata_list.append(Fdata[tick])
	Fdata=Fdata_list
	return jsonify('', render_template('/ajax/update_Fdata_model.html', Fdata=Fdata))

#MCdata AJAX route - POST
@main.route('/update_SCdata', methods=['POST'])
def updateSCdata():
	TDSession.login()
	my_file = open("symbols/smallcap.txt")
	content = my_file.read()
	SCticklist = content.split(", ")
	my_file.close()
	SCdata = TDSession.get_quotes(instruments=SCticklist)
	SCdata_list=[]
	for tick in SCticklist:
		SCdata_list.append(SCdata[tick])
	SCdata=SCdata_list
	return jsonify('', render_template('/ajax/update_SCdata_model.html', SCdata=SCdata))

#LCdata AJAX route - POST
@main.route('/update_BCdata', methods=['POST'])
def updateBCdata():
	TDSession.login()
	my_file = open("symbols/bluechip.txt")
	content = my_file.read()
	BCticklist = content.split(", ")
	my_file.close()
	BCdata = TDSession.get_quotes(instruments=BCticklist)
	BCdata_list=[]
	for tick in BCticklist:
		BCdata_list.append(BCdata[tick])
	BCdata=BCdata_list
	return jsonify('', render_template('/ajax/update_BCdata_model.html', BCdata=BCdata))

#Portfolio AJAX route 
@main.route('/update_Portfoliodata', methods=['POST'])
def updatePortfoliodata():
	TDSession.login()
	data = TDSession.get_accounts(account='all', fields=['positions'])
	return jsonify('', render_template('/ajax/update_Portfoliodata_model.html', data=data))
#######################################################################################