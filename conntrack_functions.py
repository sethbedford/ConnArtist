import subprocess
import json
import datetime
import socket
import os


def conntrack_parse(mode):
	print("MODE: " + mode)
	
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
			# print("TCP client src: " + split_line[4].split("=")[1]) # Print SRC client
			# print("TCP client dst: " + split_line[5].split("=")[1]) # Print DST client
			# print("TCP client src: " + split_line[6].split("=")[1]) # Print SPORT client
			# print("TCP client dst: " + split_line[7].split("=")[1]) # Print DPORT client

			string_return += "TCP client src: " + split_line[4].split("=")[1] + "<br/>"
			string_return += "TCP client dst: " + split_line[5].split("=")[1] + "<br/>"
			string_return += "TCP client src: " + split_line[6].split("=")[1] + "<br/>"
			string_return += "TCP client dst: " + split_line[7].split("=")[1] + "<br/>"

			try:
				# print("TCP server src: " + split_line[8].split("=")[1]) # Print SRC server
				# print("TCP server dst: " + split_line[9].split("=")[1]) # Print DST server
				# print("TCP server src: " + split_line[10].split("=")[1]) # Print SPORT server
				# print("TCP server dst: " + split_line[11].split("=")[1]) # Print DPORT server

				string_return += "TCP server src: " + split_line[8].split("=")[1] + "<br/>"
				string_return += "TCP server dst: " + split_line[9].split("=")[1] + "<br/>"
				string_return += "TCP server src: " + split_line[10].split("=")[1] + "<br/>"
				string_return += "TCP server dst: " + split_line[11].split("=")[1] + "<br/>"
			except: 
				continue
			
			mode = str(mode).strip()
			
			if ("IP" in mode):
				if (split_line[4].split("=")[1] not in IP_dict):
					json_output["nodes"].append(
					{"id":split_line[4].split("=")[1], 
					"group":0,})
					IP_dict[split_line[4].split("=")[1]] = 1;

				if (split_line[5].split("=")[1] not in IP_dict):
					json_output["nodes"].append(
					{"id":split_line[5].split("=")[1], 
					"group":1})
					IP_dict[split_line[5].split("=")[1]] = 1;

				linkExists = False
				for link in json_output["links"]:
					if link["source"] == split_line[3].split("=")[1] and link["target"] == split_line[4].split("=")[1]:
						link["weight"] = link["weight"] + 1
						linkExists = True;

				if linkExists == False:
					json_output["links"].append(
					{"source":split_line[3].split("=")[1], 
					"target":split_line[4].split("=")[1], 
					"value":2,
					"weight":1})
			
				#json_output["links"].append(
				#{"source":split_line[4].split("=")[1], 
				#"target":split_line[5].split("=")[1], 
				#"value":1})	
			
			elif ("PORT" in mode):
				destinationURL = ""
				try:
					destinationURL = socket.gethostbyaddr(split_line[5].split("=")[1])[0]
				except:
					destinationURL = "Unknown"

				if (split_line[6].split("=")[1] not in IP_dict):
					json_output["nodes"].append(
					{"id":split_line[6].split("=")[1], 
					"group":0,
					"SourceIP":split_line[4].split("=")[1],
					"DestinationIP":split_line[5].split("=")[1],
					"DestinationURL":destinationURL})
					IP_dict[split_line[6].split("=")[1]] = 1;
				else:
					for node in json_output["nodes"]:
						if node["id"] == split_line[6].split("=")[1] and node["group"] == 1:
							node["group"] = 2;

				if (split_line[7].split("=")[1] not in IP_dict):
					json_output["nodes"].append(
					{"id":split_line[7].split("=")[1], 
					"group":1,
					"SourceIP":split_line[4].split("=")[1],
					"DestinationIP":split_line[5].split("=")[1],
					"DestinationURL":destinationURL})
					IP_dict[split_line[7].split("=")[1]] = 1;
				else:
					for node in json_output["nodes"]:
						if node["id"] == split_line[6].split("=")[1] and node["group"] == 1:
							node["group"] = 2;

				linkExists = False
				for link in json_output["links"]:
					if link["source"] == split_line[6].split("=")[1] and link["target"] == split_line[7].split("=")[1]:
						link["weight"] = link["weight"] + 1
						linkExists = True;

				if linkExists == False:
					json_output["links"].append(
					{"source":split_line[6].split("=")[1], 
					"target":split_line[7].split("=")[1], 
					"value":2,
					"weight":1})

				#json_output["links"].append(
				#{"source":split_line[6].split("=")[1], 
				#"target":split_line[7].split("=")[1], 
				#"value":1})		

					

		elif split_line[0] == "udp":
			# print("UDP client src: " + split_line[3].split("=")[1]) # Print SRC client
			# print("UDP client dst: " + split_line[4].split("=")[1]) # Print DST client
			# print("UDP client src: " + split_line[5].split("=")[1]) # Print SPORT client
			# print("UDP client dst: " + split_line[6].split("=")[1]) # Print DPORT client

			string_return += "UDP client src: " + split_line[3].split("=")[1] + "<br/>"
			string_return += "UDP client dst: " + split_line[4].split("=")[1] + "<br/>"
			string_return += "UDP client src: " + split_line[5].split("=")[1] + "<br/>"
			string_return += "UDP client dst: " + split_line[6].split("=")[1] + "<br/>"

			# Need try/except for weird case where we get MAC values in UDP, no idea what causes it
			try:
				# print("UDP server src: " + split_line[7].split("=")[1]) # Print SRC server
				# print("UDP server dst: " + split_line[8].split("=")[1]) # Print DST server
				# print("UDP server src: " + split_line[9].split("=")[1]) # Print SPORT server
				# print("UDP server dst: " + split_line[10].split("=")[1]) # Print DPORT server

				string_return += "UDP client src: " + split_line[7].split("=")[1] + "<br/>"
				string_return += "UDP client dst: " + split_line[8].split("=")[1] + "<br/>"
				string_return += "UDP client src: " + split_line[9].split("=")[1] + "<br/>"
				string_return += "UDP client dst: " + split_line[10].split("=")[1] + "<br/>"
			except:
				continue

			mode = str(mode).strip()

			if("IP" in mode):
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

				linkExists = False
				for link in json_output["links"]:
					if link["source"] == split_line[3].split("=")[1] and link["target"] == split_line[4].split("=")[1]:
						link["weight"] = link["weight"] + 1
						linkExists = True;

				if linkExists == False:
					json_output["links"].append(
					{"source":split_line[3].split("=")[1], 
					"target":split_line[4].split("=")[1], 
					"value":1,
					"weight":1})

			elif("PORT" in mode):
				destinationURL = ""
				try:
					destinationURL = socket.gethostbyaddr(split_line[4].split("=")[1])[0]
				except:
					destinationURL = "Unknown"

				if (split_line[5].split("=")[1] not in IP_dict):
					json_output["nodes"].append(
					{"id":split_line[5].split("=")[1], 
					"group":0,
					"SourceIP":split_line[3].split("=")[1],
					"DestinationIP":split_line[4].split("=")[1],
					"DestinationURL":destinationURL})
					IP_dict[split_line[5].split("=")[1]] = 1;
				else:
					for node in json_output["nodes"]:
						if node["id"] == split_line[6].split("=")[1] and node["group"] == 1:
							node["group"] = 2;

				if (split_line[6].split("=")[1] not in IP_dict):
					json_output["nodes"].append(
					{"id":split_line[6].split("=")[1],
					"group":1,
					"SourceIP": split_line[3].split("=")[1],
					"DestinationIP": split_line[4].split("=")[1],
					"DestinationURL":destinationURL})
					IP_dict[split_line[6].split("=")[1]] = 1;
				else:
					for node in json_output["nodes"]:
						if node["id"] == split_line[6].split("=")[1] and node["group"] == 1:
							node["group"] = 2;
				
				linkExists = False
				for link in json_output["links"]:
					if link["source"] == split_line[5].split("=")[1] and link["target"] == split_line[6].split("=")[1]:
						link["weight"] = link["weight"] + 1
						linkExists = True;

				if linkExists == False:
					json_output["links"].append(
					{"source":split_line[5].split("=")[1], 
					"target":split_line[6].split("=")[1], 
					"value":1,
					"weight":1})

				#json_output["links"].append(
				#{"source":split_line[5].split("=")[1], 
				#"target":split_line[6].split("=")[1], 
				#"value":2,
				#"weight":1})
		else:
			continue			

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

	if "PORT" in mode:
		with open('app/static/conntrack_data_port.json', 'w') as outfile:
			json.dump(json_output, outfile)
	else:
		with open('app/static/conntrack_data.json', 'w') as outfile:
			json.dump(json_output, outfile)			

	archiveJson(json_output, mode)
	return string_return

# Copies the json generated from the conntrack data to a archive folder for recall if need be
def archiveJson(json_output, mode):

	# Check if output is same as most recent file -- don't output if sort
    files = os.listdir('app/static/PrevSnapshots')
    files.sort(reverse=1)
    if len(files) != 0:
        prevOutput = open('app/static/PrevSnapshots/' + files[0], "r")
        prevJSON = prevOutput.read()
        if(prevJSON != json_output):
            timeStampedFileName = "conntrackData-" + datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S") + "_" + str(mode) +  ".json"
            with open('app/static/PrevSnapshots/' + timeStampedFileName, 'w') as outfile:
                json.dump(json_output, outfile)
    else:
        timeStampedFileName = "conntrackData-" + datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S") + "_" + str(mode) +  ".json"
        with open('app/static/PrevSnapshots/' + timeStampedFileName, 'w') as outfile:
            json.dump(json_output, outfile)
