#!/bin/bash

source test.env/bin/activate
pip install -U pip setuptools
cd test
pip install -r requirements.txt
py.test test.py

