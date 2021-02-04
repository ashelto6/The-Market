from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
	return render_template("index.html")

@app.route('/trades')
def trades():
	return render_template("trades.html")
