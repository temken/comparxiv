#!/usr/bin/env python
import os
import pytest

from comparxiv.comparxiv import *
from comparxiv.command_line import *

@pytest.mark.parametrize("ID",["hep-ph/0612065","1709.06573","1901.04503","1905.05776"])
def test_comparxiv(ID):
	keep_temp_files = False
	show_latex_output = False
	dont_open_pdf = True
	dont_compare_equations = False
	assert compare_preprints(ID, 1, 2, keep_temp_files, show_latex_output, dont_open_pdf, dont_compare_equations)

@pytest.mark.parametrize("cmd, pdf",[
	("comparxiv --dont_open_pdf 1907.06674 1 2","1907.06674_v1v2.pdf"),
	("comparxiv --dont_open_pdf 1907.06674v3","1907.06674_v2v3.pdf"),
	("comparxiv --dont_open_pdf 1410.0314 3","1410.0314_v2v3.pdf"),
	("comparxiv --dont_open_pdf 1410.0314v1 3","1410.0314_v1v3.pdf"),
	("comparxiv --dont_open_pdf 1709.06573","1709.06573_v1v2.pdf")
])
def test_command_line(cmd, pdf):
	os.system(cmd)
	assert os.path.isfile(pdf)

