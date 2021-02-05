from flask import Flask, render_template, jsonify
from tda import auth, client
import json
import config

try:
    c = auth.client_from_token_file(config.token_path, config.api_key)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome(executable_path='/mnt/c/Users/ajshe/Desktop/projects/unJumble/chromedriver.exe') as driver:
        c = auth.client_from_login_flow(
            driver, config.api_key, config.redirect_uri, config.token_path)

app = Flask(__name__)

#homepage route
@app.route('/')
@app.route('/home')
def hello():
	return render_template("index.html")

#trades page route
@app.route('/portfolio')
def trades():
	return render_template("portfolio.html")
