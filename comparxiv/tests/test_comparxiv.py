#!/usr/bin/env python
import os

from ..comparxiv import *

def test_comparxiv():
	test_preprints = ["hep-ph/0612065","1709.06573"]
	for ID in test_preprints:
		if "/" in ID:
			diff_file = os.path.split(ID)[-1]+"_v1v2"
		else:
			diff_file = ID+"_v1v2"
		assert compare_preprints(ID, 1, 2, False, False, True)
