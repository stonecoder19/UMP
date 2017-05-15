"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app
from flask import render_template, request, redirect, url_for, flash
import smtplib
from utils.util import *


###
# Routing for your application.
###

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/api/processing',methods=['POST'])
def coordinates():
    if request.json['outer']:
        outerbounds = request.json['outer']
        print outerbounds
    if request.json['inner']:
	    innerbounds1 = request.json['inner']
	    print innerbounds1
    if request.json['inner2']:
	    innerbounds2 = request.json['inner2']
	    print innerbounds2
    print get_final_path()
    return "Success"




###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")