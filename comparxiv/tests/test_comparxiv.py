#!/usr/bin/env python
import os

from ..comparxiv import *

def test_comparxiv():
	test_preprints = ["hep-ph/0612065","1709.06573","1905.05776"]
	for ID in test_preprints:
		assert compare_preprints(ID, 1, 2, False, False, True)
