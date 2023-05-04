#!/bin/bash

curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py;
python3 get-pip.py;
pip install --no-cache-dir -r requirements.txt;
python3 setup.py;
python3 Lineu.py;
