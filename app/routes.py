from app import app
from flask import render_template, url_for
import os

from conntrack_functions import *

@app.route('/')
@app.route('/index')
def index():
	conntrack_parse()
	url = url_for('static', filename='conntrack_data.json')

	links = generateListPrevSnapshots()

	return render_template('index.html', variable=url, list=links)

@app.route('/snapshot/<fileName>')
def previousSnapshot(fileName=None):

	if fileName == None:
		return "Error: No file by that name found"

	url = url_for('static', filename="PrevSnapshots/" + fileName)
	
	links = generateListPrevSnapshots()

	return render_template('index.html', variable=url, list=links)

def generateListPrevSnapshots():
	archivedFiles = os.listdir("./app/static/PrevSnapshots/")

	links = ""	
	for file in archivedFiles:
		links += "<a href=\"" + "/snapshot/" + file + "\">" + file + "</a>" + "\n"
		links += "<br>"
	
	return links