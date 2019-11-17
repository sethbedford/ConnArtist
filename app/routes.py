from app import app
from flask import render_template, url_for
import os

from conntrack_functions import *

@app.route('/')
@app.route('/index')
def index():
	conntrack_parse("IP")
	url = url_for('static', filename='conntrack_data.json')

	links = generateListPrevSnapshots("IP")
	tooltip = 'return "SourcePort: " + d.id + "\\n" + "SourceIP: " + d.SourceIP + "\\n" + "DestinationIP: " + d.DestinationIP + "\\nDestinationURL: " + d.DestinationURL;'

	return render_template('index.html', variable=url, list=links, title=tooltip)

@app.route('/port')
def index_port():
	conntrack_parse("PORT")
	url = url_for('static', filename='conntrack_data.json')

	links = generateListPrevSnapshots("PORT")
	tooltip = 'return "SourcePort: " + d.id + "\\n" + "SourceIP: " + d.SourceIP + "\\n" + "DestinationIP: " + d.DestinationIP + "\\nDestinationURL: " + d.DestinationURL;'

	return render_template('index.html', variable=url, list=links, title=tooltip)

@app.route('/snapshot/<fileName>')
def previousSnapshot(fileName=None):

	if fileName == None:
		return "Error: No file by that name found"

	url = url_for('static', filename="PrevSnapshots/" + fileName)
	
	links = generateListPrevSnapshots("IP")
	tooltip = 'return "SourcePort: " + d.id + "\\n" + "SourceIP: " + d.SourceIP + "\\n" + "DestinationIP: " + d.DestinationIP + "\\nDestinationURL: " + d.DestinationURL;'

	return render_template('index.html', variable=url, list=links, title=tooltip)

def generateListPrevSnapshots(mode):
	archivedFiles = os.listdir("./app/static/PrevSnapshots/")

	links = ""	
	for file in archivedFiles:
		if mode in file:
			links += "<a href=\"" + "/snapshot/" + file + "\">" + file + "</a>" + "\n"
			links += "<br>"
		
	return links