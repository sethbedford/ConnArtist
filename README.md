ConnArtist
============
A browser-based [conntrack](http://conntrack-tools.netfilter.org/) visualization tool. 

Utilizes [Flask](https://www.palletsprojects.com/p/flask/), on the back-end, and [D3](https://d3js.org/) on the front-end in order to parse conntrack data and generate a force-directed graph of connections.

![ConnArtist](https://raw.githubusercontent.com/Eric-Rogers/ConnArtist/master/images/ConnArtist.png)

Features
-------

* Color coded node types and edges

* Auto-updating graph

* IP-based connection graph

* Port-based connection graph

* Ability to save and recall snapshots

* Ability to export data in a human readable format


Installation
============
First clone the repository:
``git clone https://github.com/Eric-Rogers/ConnArtist``

Install the conntrack, python (2), venv, and virtualenv packages:
``sudo apt install -y conntrack && sudo apt install -y python && sudo apt install -y python3-venv && sudo apt install -y virtualenv``

Create the virtual environment:
./createVirtualEnvironment.sh

Run the following lines as root:
``sudo bash``

Switch to the virtual environment:
``source flaskVENV/bin/activate``

Install flask if not already done on the virtual environment:
``pip install flask``

Set iptables to route through conntrack:
``iptables -A INPUT -j ACCEPT -m conntrack --ctstate NEW,ESTABLISHED,RELATED``

Set the flask app:
``export FLASK_APP=ConnArtist.py``

Run flask:
``flask run``

The graph can be viewed at ``localhost:5000``
