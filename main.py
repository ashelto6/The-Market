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
	#for large cap data 
	my_file = open("symbols/largecaps.txt")
	content = my_file.read()
	LCticklist = content.split(", ")
	my_file.close()
	LCdata = TDSession.get_quotes(instruments=LCticklist)
	LCdata_list=[]
	for tick in LCticklist:
		LCdata_list.append(LCdata[tick])
	LCdata=LCdata_list

	#for mid cap data
	my_file = open("symbols/midcaps.txt")
	content = my_file.read()
	MCticklist = content.split(", ")
	my_file.close()
	MCdata = TDSession.get_quotes(instruments=MCticklist)
	MCdata_list=[]
	for tick in MCticklist:
		MCdata_list.append(MCdata[tick])
	MCdata=MCdata_list
	
	#for penny cap data
	my_file = open("symbols/smallcaps.txt")
	content = my_file.read()
	PSticklist = content.split(", ")
	my_file.close()
	PSdata = TDSession.get_quotes(instruments=PSticklist)
	PSdata_list=[]
	for tick in PSticklist:
		PSdata_list.append(PSdata[tick])
	PSdata=PSdata_list
 
	today = date.today()
	today=today.strftime("%m/%d/%Y")
 
	return render_template("/main/index.html",  LCdata=LCdata, MCdata=MCdata, PSdata=PSdata, date=today)

#portfolio page route - GET
@main.route('/portfolio')
@login_required
def portfolio():
	data = TDSession.get_accounts(account='all', fields=['positions'])
	today = date.today()
	today=today.strftime("%m/%d/%Y")
	return render_template('/main/portfolio.html', name=current_user.first_name, data=data, date=today)
 
#watchlist page route - GET
@main.route('/watchlist')
def watchlist():
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
@main.route('/update_PSdata', methods=['POST'])
def updatePSdata():
	my_file = open("symbols/smallcaps.txt")
	content = my_file.read()
	PSticklist = content.split(", ")
	my_file.close()
	PSdata = TDSession.get_quotes(instruments=PSticklist)
	PSdata_list=[]
	for tick in PSticklist:
		PSdata_list.append(PSdata[tick])
	PSdata=PSdata_list
	return jsonify('', render_template('/ajax/update_PSdata_model.html', PSdata=PSdata))

#MCdata AJAX route - POST
@main.route('/update_MCdata', methods=['POST'])
def updateMCdata():
	my_file = open("symbols/midcaps.txt")
	content = my_file.read()
	MCticklist = content.split(", ")
	my_file.close()
	MCdata = TDSession.get_quotes(instruments=MCticklist)
	MCdata_list=[]
	for tick in MCticklist:
		MCdata_list.append(MCdata[tick])
	MCdata=MCdata_list
	return jsonify('', render_template('/ajax/update_MCdata_model.html', MCdata=MCdata))

#LCdata AJAX route - POST
@main.route('/update_LCdata', methods=['POST'])
def updateLCdata():
	my_file = open("symbols/largecaps.txt")
	content = my_file.read()
	LCticklist = content.split(", ")
	my_file.close()
	LCdata = TDSession.get_quotes(instruments=LCticklist)
	LCdata_list=[]
	for tick in LCticklist:
		LCdata_list.append(LCdata[tick])
	LCdata=LCdata_list
	return jsonify('', render_template('/ajax/update_LCdata_model.html', LCdata=LCdata))

@main.route('/update_Portfoliodata', methods=['POST'])
def updatePortfoliodata():
	data = TDSession.get_accounts(account='all', fields=['positions'])
	return jsonify('', render_template('/ajax/update_Portfoliodata_model.html', data=data))

@main.route('/update_Portfoliodata_sm', methods=['POST'])
def updatePortfoliodatasm():
	data = TDSession.get_accounts(account='all', fields=['positions'])
	return jsonify('', render_template('/ajax/update_Portfoliodata_sm_model.html', data=data))
#######################################################################################