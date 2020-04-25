#!/usr/bin/env python
import os

from ..comparxiv import *
from ..command_line import *

def test_comparxiv():
	test_preprints = ["hep-ph/0612065","1709.06573","1901.04503","1905.05776"]
	keep_temp_files = False
	show_latex_output = False
	dont_open_pdf = True
	dont_compare_equations = False
	for ID in test_preprints:
		assert compare_preprints(ID, 1, 2, keep_temp_files, show_latex_output, dont_open_pdf, dont_compare_equations)

def test_command_line():
	tests = [
		["comparxiv --dont_open_pdf 1907.06674 1 2","1907.06674_v1v2.pdf"],
		["comparxiv --dont_open_pdf 1907.06674v3","1907.06674_v2v3.pdf"],
		["comparxiv --dont_open_pdf 1410.0314 3","1410.0314_v2v3.pdf"],
		["comparxiv --dont_open_pdf 1410.0314v1 3","1410.0314_v1v3.pdf"],
		["comparxiv --dont_open_pdf 1709.06573","1709.06573_v1v2.pdf"]
	]

	for test in tests:
		os.system(test[0])
		assert os.path.isfile(test[1])

