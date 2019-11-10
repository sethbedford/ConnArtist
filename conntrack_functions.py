import subprocess
import json
import time

def conntrack_parse():
	p = subprocess.check_output(["conntrack", "-L"])
	p = str(p)
	p = p.replace("\\n", "\n")
	p = p.replace("b\'", "")
	p = p.replace("\'", "")

	p = p.split("\n")

	for line in p:
		print(line)

	string_return = ""

	json_output = {}
	json_output["nodes"] = []
	json_output["links"] = []

	IP_dict = {}

	for line in p:
		split_line = line.split()
		if len(split_line) == 0:
			break

		
		if split_line[0] == "tcp":
			print("TCP client src: " + split_line[4].split("=")[1]) # Print SRC client
			print("TCP client dst: " + split_line[5].split("=")[1]) # Print DST client
			print("TCP client src: " + split_line[6].split("=")[1]) # Print SPORT client
			print("TCP client dst: " + split_line[7].split("=")[1]) # Print DPORT client

			string_return += "TCP client src: " + split_line[4].split("=")[1] + "<br/>"
			string_return += "TCP client dst: " + split_line[5].split("=")[1] + "<br/>"
			string_return += "TCP client src: " + split_line[6].split("=")[1] + "<br/>"
			string_return += "TCP client dst: " + split_line[7].split("=")[1] + "<br/>"

			try:
				print("TCP server src: " + split_line[8].split("=")[1]) # Print SRC server
				print("TCP server dst: " + split_line[9].split("=")[1]) # Print DST server
				print("TCP server src: " + split_line[10].split("=")[1]) # Print SPORT server
				print("TCP server dst: " + split_line[11].split("=")[1]) # Print DPORT server

				string_return += "TCP server src: " + split_line[8].split("=")[1] + "<br/>"
				string_return += "TCP server dst: " + split_line[9].split("=")[1] + "<br/>"
				string_return += "TCP server src: " + split_line[10].split("=")[1] + "<br/>"
				string_return += "TCP server dst: " + split_line[11].split("=")[1] + "<br/>"
			except: 
				continue

			if (split_line[4].split("=")[1] not in IP_dict):
				json_output["nodes"].append(
		 		{"id":split_line[4].split("=")[1], 
		 		"group":0})
				IP_dict[split_line[4].split("=")[1]] = 1;

			if (split_line[5].split("=")[1] not in IP_dict):
				json_output["nodes"].append(
		 		{"id":split_line[5].split("=")[1], 
		 		"group":1})
				IP_dict[split_line[5].split("=")[1]] = 1;

			json_output["links"].append(
			{"source":split_line[4].split("=")[1], 
			"target":split_line[5].split("=")[1], 
			"value":1})			

		elif split_line[0] == "udp":
			print("UDP client src: " + split_line[3].split("=")[1]) # Print SRC client
			print("UDP client dst: " + split_line[4].split("=")[1]) # Print DST client
			print("UDP client src: " + split_line[5].split("=")[1]) # Print SPORT client
			print("UDP client dst: " + split_line[6].split("=")[1]) # Print DPORT client

			string_return += "UDP client src: " + split_line[3].split("=")[1] + "<br/>"
			string_return += "UDP client dst: " + split_line[4].split("=")[1] + "<br/>"
			string_return += "UDP client src: " + split_line[5].split("=")[1] + "<br/>"
			string_return += "UDP client dst: " + split_line[6].split("=")[1] + "<br/>"

			# Need try/except for weird case where we get MAC values in UDP, no idea what causes it
			try:
				print("UDP server src: " + split_line[7].split("=")[1]) # Print SRC server
				print("UDP server dst: " + split_line[8].split("=")[1]) # Print DST server
				print("UDP server src: " + split_line[9].split("=")[1]) # Print SPORT server
				print("UDP server dst: " + split_line[10].split("=")[1]) # Print DPORT server

				string_return += "UDP client src: " + split_line[7].split("=")[1] + "<br/>"
				string_return += "UDP client dst: " + split_line[8].split("=")[1] + "<br/>"
				string_return += "UDP client src: " + split_line[9].split("=")[1] + "<br/>"
				string_return += "UDP client dst: " + split_line[10].split("=")[1] + "<br/>"
			except:
				continue

			if (split_line[3].split("=")[1] not in IP_dict):
				json_output["nodes"].append(
		 		{"id":split_line[3].split("=")[1], 
		 		"group":0})
				IP_dict[split_line[3].split("=")[1]] = 1;

			if (split_line[4].split("=")[1] not in IP_dict):
				json_output["nodes"].append(
		 		{"id":split_line[4].split("=")[1], 
		 		"group":1})
				IP_dict[split_line[4].split("=")[1]] = 1;

			json_output["links"].append(
			{"source":split_line[3].split("=")[1], 
			"target":split_line[4].split("=")[1], 
			"value":2})
		else:
			continue			


		print()
		string_return += "<br/>"

	# Generate json that D3 likes
	# json_output = {}
	# json_output["nodes"] = []
	
	# json_output["nodes"].append(
	# 	{"id":"REPLACE", 
	# 	"group":"REPLACE"})

	# json_output["links"] = []
	
	# json_output["links"].append(
	# 	{"source":"REPLACE", 
	# 	"target":"REPLACE", 
	# 	"value":"REPLACE"})

	with open('app/static/conntrack_data.json', 'w') as outfile:
		json.dump(json_output, outfile)

	archiveJson(json_output)
	return string_return

# Copies the json generated from the conntrack data to a archive folder for recall if need be
def archiveJson(json_output):

	# The timestamp we use is nanoseconds since epoch to avoid overwriting if quick refreshes
	timeStampedFileName = "conntrackData-" + str(time.time_ns()) + ".json"

	with open('app/static/PrevSnapshots/' + timeStampedFileName, 'w') as outfile:
		json.dump(json_output, outfile)