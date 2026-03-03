#!/usr/bin/env/python3
import sys
import os

#Ensure project root is in the Python paat
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from main import run

if __name__ =="__main__":
	run()

