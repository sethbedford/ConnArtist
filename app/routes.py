from app import app
from flask import render_template, url_for
import os

from conntrack_functions import *

@app.route('/')
@app.route('/index')
@app.route('/ip')
def index():
	conntrack_parse("IP")
	url = url_for('static', filename='conntrack_data.json')

	links = generateListPrevSnapshots("IP")
	tooltip = 'return "SourcePort: " + d.id + "\\n" + "SourceIP: " + d.SourceIP + "\\n" + "DestinationIP: " + d.DestinationIP + "\\nDestinationURL: " + d.DestinationURL;'

	return render_template('index.html', variable=url, list=links, title=tooltip, mode="IP")

@app.route('/port')
def index_port():
	conntrack_parse("PORT")
	url = url_for('static', filename='conntrack_data_port.json')

	links = generateListPrevSnapshots("PORT")
	tooltip = 'return "SourcePort: " + d.id + "\\n" + "SourceIP: " + d.SourceIP + "\\n" + "DestinationIP: " + d.DestinationIP + "\\nDestinationURL: " + d.DestinationURL;'

	return render_template('index.html', variable=url, list=links, title=tooltip, mode="PORT")

@app.route('/snapshot/<fileName>')
def previousSnapshot(fileName=None):

	if fileName == None:
		return "Error: No file by that name found"

	url = url_for('static', filename="PrevSnapshots/" + fileName)
	m = ""
	if "IP" in fileName:
	    m = "IP"
	else:
	    m = "PORT"
	links = generateListPrevSnapshots(m)
	tooltip = 'return "SourcePort: " + d.id + "\\n" + "SourceIP: " + d.SourceIP + "\\n" + "DestinationIP: " + d.DestinationIP + "\\nDestinationURL: " + d.DestinationURL;'

	return render_template('save.html', variable=url, list=links, title=tooltip, mode=m.lower())

def generateListPrevSnapshots(mode):
	archivedFiles = os.listdir("./app/static/PrevSnapshots/")
	archivedFiles.sort(reverse=1)
	links = ""
	for file in archivedFiles:
		if mode in file:
			links += "<a href=\"" + "/snapshot/" + file + "\">" + file + "</a>" + "\n"
			links += "<br>"
		
	return links