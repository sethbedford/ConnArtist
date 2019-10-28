from app import app
from flask import render_template

from conntrack_functions import *

@app.route('/')
@app.route('/index')
def index():
	conntrack_parse()
	return render_template('index.html')
