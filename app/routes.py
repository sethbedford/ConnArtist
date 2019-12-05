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
	url = url_for('static', filename='conntrack_data.json')
	return render_template('index.html', variable=url, mode="IP", view="LIVE")

@app.route('/port')
def index_port():
	url = url_for('static', filename='conntrack_data_port.json')
	return render_template('index.html', variable=url, mode="PORT", view="LIVE")

@app.route('/generate')
def generate():
	mode = request.args.get('mode')
	view = request.args.get('view')
	if "LIVE" in view:
		conntrack_parse(mode)
	links = generateListPrevSnapshots(mode)
	return json.dumps(links)

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
	return render_template('index.html', variable=url, mode=m, view="SAVE")

def generateListPrevSnapshots(mode):
	archivedFiles = os.listdir("./app/static/PrevSnapshots/")
	archivedFiles.sort(reverse=1)
	filteredFiles = list(filter(lambda x: mode in x, archivedFiles))
	links = {}
	links["filenames"] = []
	for file in filteredFiles[25:]:
		os.remove("./app/static/PrevSnapshots/" + file)
	for file in filteredFiles[:25]:
		if mode in file:
			links["filenames"].append(file);
		
	return links