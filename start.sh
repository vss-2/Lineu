#!/bin/bash

curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py;
python get-pip.py;
pip install --no-cache-dir -r requirements.txt;
python setup.py;
python Lineu.py;
