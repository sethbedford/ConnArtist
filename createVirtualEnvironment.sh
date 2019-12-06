#!/bin/sh

python3 -m venv flaskVENV
virtualenv flaskVENV/
mkdir -p app/static/PrevSnapshots
mkdir -p app/static/saves
mkdir -p app/static/exports
touch app/static/connartist_data_port.json