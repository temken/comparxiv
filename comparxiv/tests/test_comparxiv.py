#!/usr/bin/env python
import os

from ..comparxiv import *

def test_comparxiv():
	test_preprints = ["hep-ph/0612065","1709.06573","1901.04503","1905.05776"]
	keep_temp_files = False
	show_latex_output = False
	dont_open_pdf = True
	dont_compare_equations = False
	for ID in test_preprints:
		assert compare_preprints(ID, 1, 2, keep_temp_files, show_latex_output, dont_open_pdf, dont_compare_equations)
