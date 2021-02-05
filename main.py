from flask import Flask, render_template

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
