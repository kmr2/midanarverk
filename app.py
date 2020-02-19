from flask import Flask, render_template, request, json
from datetime import datetime
from jinja2 import ext
import os
import urllib.request

app = Flask(__name__)

app.jinja_env.add_extension(ext.do)

with urllib.request.urlopen("https://apis.is/petrol/") as url:
    data = json.loads(url.read().decode())


def format_time(data):
    return datetime.strptime(data, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d. %m. %Y. %H:%M:%S")

app.jinja_env.filters['format_time'] = format_time

def minPetrol():
    minPetrolPrice = 1000
    company= None
    address = None
    lst = data['results']

    for i in lst:
        if i['bensin95'] is not None:
            if i['bensin95'] < minPetrolPrice:
                company = i['company']
                address = i['name']
                minPetrolPrice = i['bensin95']
    return [ minPetrolPrice, company, address ]

def minDiesel():
    minDieselPrice = 1000
    company= None
    address = None
    lst = data['results']

    for i in lst:
        if i['diesel'] is not None:
            if i['diesel'] < minDieselPrice:
                company = i['company']
                address = i['name']
                minDieselPrice = i['diesel']
    return [ minDieselPrice, company, address ]





@app.route('/')
def home():
    return render_template('index.html', data=data, MinP=minPetrol(), MinD=minDiesel())

#fyrirtæki
@app.route('/company/<company>')
def comp(company):
    return render_template('company.html', data=data, com=company)

#bensinstöð fyrirtækar
@app.route('/moreinfo/<key>')
def info(key):
    return render_template('moreinfo.html', data=data, k=key)

@app.errorhandler(404)
def pagenotfound(error):
    return render_template('pagenotfound.html'), 404


if __name__ == '__main__':
    app.run(debug=True)