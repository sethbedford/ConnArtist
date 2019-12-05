from app import app
from flask import render_template, url_for, request
import datetime
import os

from conntrack_functions import *

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
@app.route('/index')
@app.route('/ip')
def index():
	conntrack_parse("IP")
	url = url_for('static', filename='conntrack_data.json')

	links = generateListPrevSnapshots("IP")
	tooltip = 'return "IP: " + d.id'

	return render_template('index.html', variable=url, list=links, title=tooltip, mode="IP")

@app.route('/port')
def index_port():
	conntrack_parse("PORT")
	url = url_for('static', filename='conntrack_data_port.json')

	links = generateListPrevSnapshots("PORT")
	tooltip = 'return "Port: " + d.id'

	return render_template('index.html', variable=url, list=links, title=tooltip, mode="PORT")

@app.route('/export', methods=['POST'])
def export():
	mode = request.form.get('mode')
	node = request.form.get('node')
	filename = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S") + "_" + mode + "_" + node + ".data"
	if request.method == 'POST':
		data = request.form.get('data')
		f = open("app/static/exports/" + filename, "w")
		f.write(data)
		f.close()
	return filename

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
	filteredFiles = filter(lambda x: mode in x, archivedFiles)
	links = ""
	for file in filteredFiles[:25]:
		if mode in file:
			links += "<a href=\"" + "/snapshot/" + file + "\">" + file + "</a>" + "\n"
			links += "<br>"
		
	return links