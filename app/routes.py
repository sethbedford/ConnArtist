from app import app
from flask import render_template, url_for, request
import datetime
import os

from conntrack_functions import *

@app.route('/')
@app.route('/index')
@app.route('/ip')
def index():
	return render_template('index.html', mode="IP", view="LIVE")

@app.route('/port')
def index_port():
	return render_template('index.html', mode="PORT", view="LIVE")

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
		f = open("app/static/exports/" + filename, "w+")
		f.write(data)
		f.close()
	return filename

@app.route('/exports')
def exports():
	exportFiles = os.listdir("./app/static/exports/")
	exportFiles.sort(reverse=1)
	exportFilesOutput = ""
	for file in exportFiles:
		exportFilesOutput += "<a href=\"javascript:getExport('" + file + "');\">" + file + "</a><br>"
	return render_template('export.html', filenames=exportFilesOutput)

@app.route("/getExport")
def getExport():
	filename = request.args.get('file')
	filePath = "./app/static/exports/" + filename
	f = open(filePath, "r")
	output = f.read()
	f.close()
	return output.replace("\n", "<br>")

@app.route('/save', methods=['POST'])
def save():
	filename = request.form.get('filename')
	filepath = "./app/static/PrevSnapshots/" + filename
	newFile = "./app/static/saves/" + filename
	of = open(filepath, "r")
	fileContents = of.read();
	of.close()
	if request.method == 'POST':
		f = open(newFile, "w+")
		f.write(fileContents)
		f.close()
	return newFile


@app.route('/saves')
def saves():
	savedFiles = os.listdir("./app/static/saves/")
	savedFiles.sort(reverse=1)
	saveFilesOutput = ""
	for file in savedFiles:
		saveFilesOutput += "<a href='/snapshot/" + file + "'>" + file[file.index("-")+1:] + "</a><br>"
	return render_template('save.html', filenames=saveFilesOutput)

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