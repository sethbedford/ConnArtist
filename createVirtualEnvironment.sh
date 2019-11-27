#!/bin/sh

python3 -m venv flaskVENV
virtualenv flaskVENV/
mkdir -p app/static/PrevSnapshots
touch app/static/connartist_data_port.json
