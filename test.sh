#!/bin/bash

. test.env/bin/activate
cd test
pip install -r requirements.txt
py.test test.py

