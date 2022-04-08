#!/usr/bin/env python

import os
import sys
import shutil

import arxiv
import requests

from sys import platform
from tqdm import tqdm
from os.path import join


version = '0.1.8'
author = 'Timon Emken'
year = '2020'

temp_folder = ".temp_comparxiv"
def compare_preprints(arxiv_ID, version_a, version_b,keep_temp,show_latex_output,dont_open_pdf,dont_compare_equations):
	check_arguments(arxiv_ID, version_a, version_b)
	print_title(arxiv_ID, version_a, version_b)

	#Check if old or new arxiv ID
	ID_a = arxiv_ID+"v"+str(version_a)
	ID_b = arxiv_ID+"v"+str(version_b)

	#Create folder for temporary files
	if os.path.exists(temp_folder) == False:
		os.mkdir(temp_folder)

	temp_folder_a = join(temp_folder, 'temp_' + ID_a)
	temp_folder_b = join(temp_folder, 'temp_' + ID_b)
	diff_file = os.path.split(arxiv_ID)[-1]+"_v"+str(version_a)+"v"+str(version_b)
	diff_file_tex = diff_file + ".tex"
	diff_file_bbl = diff_file + ".bbl"
	diff_file_pdf = diff_file + ".pdf"

	print_paper_information(arxiv_ID,version_a,version_b)

	#1. Download and unpack files
	print("1.) Download and unpack source files:")
	download_from_arxiv(arxiv_ID,version_a)
	download_from_arxiv(arxiv_ID,version_b)

	unpack_source_files(arxiv_ID,version_a,temp_folder_a)
	unpack_source_files(arxiv_ID,version_b,temp_folder_b)

	#2. Identify the .tex and .bbl files.
	#2.1 tex files
	print("\n2.1) Identify master tex files:")
	master_file_a = identify_master_tex_file(temp_folder_a,arxiv_ID)
	master_file_b = identify_master_tex_file(temp_folder_b,arxiv_ID)
	#2.2 bbl files
	print("\n2.2) Identify bbl files:")
	bbl_file_a = identify_bbl_file(temp_folder_a,arxiv_ID)
	bbl_file_b = identify_bbl_file(temp_folder_b,arxiv_ID)

	#3. Latexdiff
	#3.1 tex files 
	print("\n3.1) Run latexdiff on the tex files.")

	latexdiff_command_tex = "latexdiff "
	if show_latex_output == False:
		latexdiff_command_tex += "--ignore-warnings "
	if dont_compare_equations:
		latexdiff_command_tex += "--math-markup=0 "
	
	latexdiff_command_tex += join(temp_folder_a, master_file_a) + " " + join(temp_folder_b,master_file_b) + ">" + join(temp_folder_b, diff_file_tex)

	os.system(latexdiff_command_tex)

	#3.2 Try to run latexdiff on bbl.
	if bbl_file_a != None and bbl_file_b != None:
		print("\n3.2) Run latexdiff on the bbl files.")
		latexdiff_command_bbl = "latexdiff "
		if show_latex_output == False:
			latexdiff_command_bbl += "--ignore-warnings "
		
		latexdiff_command_bbl += join(temp_folder_a, bbl_file_a) + " " + join(temp_folder_b, bbl_file_b) + ">" + join(temp_folder_b, diff_file_bbl)
		os.system(latexdiff_command_bbl)

	#4. Run pdflatex
	print("\n4.) Generate a pdf with pdflatex.")
	Generate_PDF(diff_file_tex,temp_folder_b,show_latex_output)

	#5. If unsuccessful, try again with a copy of the version b .bbl file.
	if bbl_file_b != None and os.path.isfile( join(temp_folder_b,diff_file_pdf) ) == False:
		print("\tWarning: No pdf could be generated. Copy the .bbl file of version b and try again.")
		shutil.copyfile( join(temp_folder_b, bbl_file_b), join(temp_folder_b, diff_file_bbl))
		Generate_PDF(diff_file_tex,temp_folder_b,show_latex_output)
	
	success = False;
	if os.path.isfile( join(temp_folder_b, diff_file_pdf)):
		success = True
	#6. Compare figures
	# todo

	#7. If successful copy the .pdf.
	if success:
		os.rename( join(temp_folder_b, diff_file_pdf), join(diff_file_pdf) )
		if dont_open_pdf == False:
			if platform == "linux" or platform == "linux2":
				os.system("xdg-open "+diff_file_pdf)
			elif platform == "darwin":
				os.system("open "+diff_file_pdf)
			elif platform == "win32":
				os.startfile(diff_file_pdf)
		print("\nSuccess!")

	else:
		print("\nFailure! No pdf file could be generated.\nTroubleshooting:")
		print("\t1.) To see more terminal output run:\n\t\t'comparxiv --show_latex_output %s %i %i'" % (arxiv_ID, version_a, version_b))
		print("\t2.) In some cases latex math environments cause problems with latexdiff. Try running:\n\t\t'comparxiv --dont_compare_equations %s %i %i'" % (arxiv_ID, version_a, version_b))
	
	#8. Delete temporary files
	if keep_temp == False:
		shutil.rmtree(temp_folder)

	return success

def print_paper_information(arxiv_ID,vA,vB):
	to_id = lambda v: '{}v{}'.format(arxiv_ID, str(v))
	papers = list_papers([to_id(vA),to_id(vB)])
	if papers[0].title != papers[1].title:
		print("New title:\t%s" % papers[1].title)
		print("Old title:\t%s" % papers[0].title)
	else:
		print("Title:\t\t%s" % papers[1].title)
	if len(papers[1].authors) == 1:
		print("Author:\t\t%s\n" % papers[1].authors[0].name)
	elif len(papers[1].authors) > 6:
		print("Authors:\t%s et al.\n" % papers[1].authors[0].name)
	else:
		print("Authors:\t",", " . join([a.name for a in papers[1].authors]),"\n")

def check_arguments(arxiv_ID,vA,vB):
	#1. Check for identical versions
	if vA == vB:
		print("Error:\tVersions to compare are identical.")
		os.abort()
	#2. Check if paper exists and has multiple versions.
	latest_version = latest_available_version(arxiv_ID)
	if latest_version == 1:
		print("Error: The paper [%s] has only one version." % (arxiv_ID))
		os.abort()
	#3. Check existence of versions: If none or only one of the versions can be found, generate some meaningful error message.
	elif vA > latest_version or vB > latest_version:
		if vA > latest_version and vB > latest_version:
			missing_version = "v%i or v%i"%(vA,vB)
			suggestion_a = latest_version-1
			suggestion_b = latest_version
		elif vA > latest_version:
			missing_version = "v%i"%(vA)
			suggestion_a = latest_version
			if vB == latest_version:
				suggestion_b = vB - 1
			else:
				suggestion_b = vB 
		elif vB > latest_version:
			missing_version = "v%i"%(vB)
			suggestion_b = latest_version
			if vA == latest_version:
				suggestion_a = vA - 1
			else:
				suggestion_a = vA 
		print("Error:\tThe preprint [%s] does not have a version %s. The latest available version is v%i.\n\tTry running 'comparxiv %s %i %i'." % (arxiv_ID,missing_version,latest_version,arxiv_ID,suggestion_a,suggestion_b))
		os.abort()	

def latest_available_version(arxiv_ID):
	papers = list_papers([arxiv_ID])
	if len(papers) == 0:
		print("Error: The paper [%s] cannot be found on the preprint server." % (arxiv_ID))
		os.abort()
	return int(papers[0].get_short_id().split("v")[-1])

def Generate_PDF(tex_file, folder, show_latex_output):
	owd = os.getcwd()
	os.chdir(folder)
	pdflatex_command = "pdflatex -interaction=nonstopmode " + tex_file
	if show_latex_output == False:
		if platform == "win32":
			pdflatex_command += " > nul 2>&1"
		else:
			pdflatex_command += " 2>&1 > /dev/null"
	os.system(pdflatex_command)
	os.system(pdflatex_command)
	os.chdir(owd)

def list_papers(ids):
	try:
		return list(arxiv.Search(id_list=ids).results())
	except AttributeError:
		# NOTE(lukasschwab): see lukasschwab/arxiv.py#80.
		return []

#Download the files from the preprint server, if it hasn't been done before.
def download_from_url(url, destination):
	file_size = int(requests.head(url).headers["Content-Length"])
	if os.path.exists(destination):
		first_byte = os.path.getsize(destination)
	else:
		first_byte = 0
	if first_byte >= file_size:
		return file_size
	header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
	pbar = tqdm(
		total=file_size, initial=first_byte,
		unit='B', unit_scale=True, desc=url.split('/')[-1])
	req = requests.get(url, headers=header, stream=True)
	with(open(destination, 'ab')) as f:
		for chunk in req.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)
				pbar.update(1024)
	pbar.close()
	return file_size


def download_from_arxiv(arxiv_ID,version):
	#Check if old or new arxiv ID
	if "/" in arxiv_ID:
		filepath = join(temp_folder, os.path.split(arxiv_ID)[-1]+"v"+str(version))
	else:
		filepath = join(temp_folder, arxiv_ID+"v"+str(version))
	if os.path.isfile(filepath) == False:
		url="https://arxiv.org/src/"+arxiv_ID+"v"+str(version)
		download_from_url(url,filepath)
	else:
		print("\tDownload of source files for [%sv%i] not necessary." % (arxiv_ID, version))

#Unpack the archived files to a temporary folder
def unpack_source_files(arxiv_ID,version,path_destination):
	version_ID = arxiv_ID + "v" + str(version)
	#Check if old or new arxiv ID
	if "/" in arxiv_ID:
		path_source = join(temp_folder, os.path.split(version_ID)[-1])
	else:
		path_source = join(temp_folder, version_ID)
	# Create folder for temporary files
	if os.path.isfile(path_source) and os.path.exists(path_destination) == False:
		os.makedirs(path_destination)
	# Unpack files
	os.system('tar -xzf '+path_source +' -C '+ path_destination)

def identify_master_tex_file(path,arxiv_ID):
	master_file = None
	tex_files = []
	files = os.listdir(path)
	for file in files:
		if file.endswith(".tex") and not (file.startswith(arxiv_ID) or file.startswith(os.path.split(arxiv_ID)[-1])):
			tex_files.append(file)
	if len(tex_files) > 1:
		for file in tex_files:
			with open( join(path,file) ) as f:
				if 'begin{document}' in f.read():
					master_file = file
					break
	elif len(tex_files) == 1:
		master_file = tex_files[0]
	elif len(tex_files) == 0 and len(files)==1:
		master_file = file + ".tex"
		os.rename( join(path, file), join(path, master_file))
	if master_file == None:
		print("Error in identify_master_tex_file(): Among the %i tex files, no master file could be identified." % len(tex_files))
		os.abort()
	else:
		print("\t%sv%s:\t%s" % (arxiv_ID, path.split('v')[-1], master_file))
		return master_file

def identify_bbl_file(path, arxiv_ID):
	# Possibility a: A .bbl file exists.
	for file in os.listdir(path):
		if file.endswith('.bbl') and not file.startswith(arxiv_ID):
			bbl_file = file
			break
	# Possibility b: No .bbl file exists.
	else:
		bbl_file = None
	print("\t%sv%s:\t%s" % (arxiv_ID, path.split('v')[-1], bbl_file))
	return bbl_file

def print_title(ID,v1,v2):
	asci_title = "                                    __  ___       \n  ___ ___  _ __ ___  _ __   __ _ _ _\ \/ (_)_   __\n / __/ _ \| '_ ` _ \| '_ \ / _` | '__\  /| \ \ / /\n| (_| (_) | | | | | | |_) | (_| | |  /  \| |\ V / \n \___\___/|_| |_| |_| .__/ \__,_|_| /_/\_\_| \_/  \n                    |_|                           "
	print(asci_title)
	print("Version %s                by %s (%s)" % (version, author, year))
	print("\nCompare [arXiv:%s]: v%i vs v%i\n" % (ID,v1,v2))

if __name__ == "__main__":
	arxiv_ID = str(sys.argv[1])
	version_a = int(sys.argv[2])
	version_b = int(sys.argv[3])
	keep_temp = False
	show_latex_output = False
	dont_open_pdf = False
	dont_compare_equations = False
	compare_preprints(arxiv_ID,version_a,version_b,keep_temp,show_latex_output,dont_open_pdf,dont_compare_equations)
