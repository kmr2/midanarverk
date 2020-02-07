from flask import Flask, render_template, request, json
from datetime import datetime
from jinja2 import ext
import os
import urllib.request

app = Flask(__name__)

app.jinja_env.add_extension(ext.do)

with urllib.request.urlopen("https://apis.is/petrol/") as url:
    data = json.loads(url.read().decode())

@app.route('/')
def home():
    return render_template('index.html', data=data)

@app.route('/company/<company>')
def comp(company):
    return render_template('company.html', data=data, com=company)

@app.errorhandler(404)
def pagenotfound(error):
    return render_template('pagenotfound.html'), 404


if __name__ == '__main__':
    app.run(debug=True)