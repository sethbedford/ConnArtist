import subprocess

p = subprocess.check_output(["conntrack", "-L"])
p = str(p)
p = p.replace("\\n", "\n")
p = p.replace("b\'", "")
p = p.replace("\'", "")

p = p.split("\n")

for line in p:
	print(line)


for line in p:
	split_line = line.split()
	if len(split_line) == 0:
		break

	
	if split_line[0] == "tcp":
		print("TCP client src: " + split_line[4].split("=")[1]) # Print SRC client
		print("TCP client dst: " + split_line[5].split("=")[1]) # Print DST client
		print("TCP client src: " + split_line[6].split("=")[1]) # Print SPORT client
		print("TCP client dst: " + split_line[7].split("=")[1]) # Print DPORT client


		print("TCP server src: " + split_line[8].split("=")[1]) # Print SRC server
		print("TCP server dst: " + split_line[9].split("=")[1]) # Print DST server
		print("TCP server src: " + split_line[10].split("=")[1]) # Print SPORT server
		print("TCP server dst: " + split_line[11].split("=")[1]) # Print DPORT server

	elif split_line[0] == "udp":
		print("UDP client src: " + split_line[3].split("=")[1]) # Print SRC client
		print("UDP client dst: " + split_line[4].split("=")[1]) # Print DST client
		print("UDP client src: " + split_line[5].split("=")[1]) # Print SPORT client
		print("UDP client dst: " + split_line[6].split("=")[1]) # Print DPORT client


		print("UDP server src: " + split_line[7].split("=")[1]) # Print SRC server
		print("UDP server dst: " + split_line[8].split("=")[1]) # Print DST server
		print("UDP server src: " + split_line[9].split("=")[1]) # Print SPORT server
		print("UDP server dst: " + split_line[10].split("=")[1]) # Print DPORT server

	print()
