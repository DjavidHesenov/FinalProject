from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/log')
def login():
    pass

@app.route('/reg')
def register():
    return render_template("reg.html")
    

@app.route('/')
def register1():
    return render_template("reg.html")
    

if __name__ == "__main__":
    app.run(debug=True)

