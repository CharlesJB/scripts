#!/usr/bin/env python
# encoding: utf-8
# author: Charles Joly Beauparlant
# 2014-02-27

"""
Usage:

Check_SampleSheet.py <sample_sheet>
	sample_sheet: File containing all the information for a run.

"""

# Check if quotes are present and add them if necessary
def add_quotes(token):
	to_return = ""
	if token[0] != '"':
		to_return = '"'
	to_return += token
	if token[len(token)-1] != '"':
		to_return += '"'
	return(to_return)

import sys

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print(__doc__)
		sys.exit(1)

	sample_sheet = sys.argv[1]

	header_parsed = False
	for line in open(sample_sheet):
		to_print = ""
		if header_parsed == False:
			first_token = True
			tokens = line.strip().split(",")
			for token in tokens:
				if first_token != True:
					to_print += ',' + add_quotes(token)
				else:
					to_print += add_quotes(token)
					first_token = False
			header_parsed = True
		else:
			to_print = line.strip().replace('"','')
		print(to_print)
