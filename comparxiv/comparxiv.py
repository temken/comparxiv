#!/usr/bin/env python

import os
import sys
import requests

from tqdm import tqdm

version = '1.0'
author = 'Timon Emken'
year = '2020'

def compare_preprints(arxiv_ID, version_a, version_b,keep_temp,show_latex_output,dont_open_pdf):
	ID_a = arxiv_ID+"v"+str(version_a)
	ID_b = arxiv_ID+"v"+str(version_b)
	temp_folder_a = './.temp_'+ID_a+'/'
	temp_folder_b = './.temp_'+ID_b+'/'
	diff_file = arxiv_ID+"_v"+str(version_a)+"v"+str(version_b)

	#1. Download and unpack files
	download_from_arxiv(ID_a)
	unpack_source_files(ID_a)
	download_from_arxiv(ID_b)
	unpack_source_files(ID_b)

	#2. Run latexdiff
	#2.1 Identify the master tex files
	master_file_a = identify_master_tex_file(temp_folder_a,arxiv_ID)
	master_file_b = identify_master_tex_file(temp_folder_b,arxiv_ID)

	#2.2 Identify or create a bbl file.
	bbl_file_a = identify_bbl_file(temp_folder_a,arxiv_ID)
	bbl_file_b = identify_bbl_file(temp_folder_b,arxiv_ID)

	#2.3 Run latexdiff on the .bbl files if they are included.
	
	# if bbl_file_a != None and bbl_file_b != None:
	# 	print("\nRun latexdiff on .bbl files:")
	# 	print("\t",temp_folder_a+bbl_file_a)
	# 	print("\t",temp_folder_b+bbl_file_b)
	# 	os.system("latexdiff --append-textcmd=field "+temp_folder_a+bbl_file_a+" "+temp_folder_b+bbl_file_b+">"+temp_folder_b+diff_file+".bbl")

	if bbl_file_b!= None:
		os.system("cp "+ temp_folder_b + bbl_file_b + " " +temp_folder_b+diff_file+".bbl")

	#2.4 Run latexdiff on the tex files
	print("\nRun latexdiff on .tex files:")
	print("\t",temp_folder_a+master_file_a)
	print("\t",temp_folder_b+master_file_b)
	os.system("latexdiff "+temp_folder_a+master_file_a+" "+temp_folder_b+master_file_b+">"+temp_folder_b+diff_file+".tex")

	#3. Compile the files to a pdf
	print("\nCompile .tex file via pdflatex via")
	os.chdir(temp_folder_b)
	pdflatex_command = "pdflatex -interaction=nonstopmode "+diff_file+".tex"
	if show_latex_output == False:
		pdflatex_command += " 2>&1 > /dev/null"
	print("\t",pdflatex_command)
	os.system(pdflatex_command)
	os.system(pdflatex_command)
	os.system("mv " + diff_file+".pdf" + " ../" + diff_file+".pdf")
	os.chdir("..")

	# os.chdir(temp_folder_b)
	# os.system("pdflatex -interaction=nonstopmode -halt-on-error "+diff_file+".tex")
	# os.system("pdflatex -interaction=nonstopmode -halt-on-error "+diff_file+".tex")
	# os.system("mv " + diff_file+".pdf" + " ../" + diff_file+".pdf")
	# os.chdir("..")

	#3. Compare references.

	#4. Extract comments

	#5. Compare figures

	#6. Delete temporary files
	if keep_temp == False:
		remove_temporary_files(arxiv_ID)

	#7. Open PDF
	if os.path.isfile(diff_file+".pdf"):
		if dont_open_pdf == False:
			print("\nOpen the pdf.")
			os.system("open "+diff_file+".pdf")
		print("\nFinished: success.")
	else:
		print("\nFinished: failure.\n\tNo pdf file could be generated.")

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


def download_from_arxiv(version_ID):
	filepath = "./"+version_ID
	if os.path.isfile(filepath) == False:
		url="https://arxiv.org/e-print/"+version_ID
		download_from_url(url,filepath)
	else:
		print("Download of source files for "+version_ID+" not necessary.")

#Unpack the archived files to a temporary folder
def unpack_source_files(version_ID):
	path_source = "./"+version_ID
	# Create folder for temporary files
	path_destination = './.temp_'+version_ID+'/'
	print("Unpack source files of",version_ID,"to",path_destination,"\n")
	if os.path.isfile(path_source) and os.path.exists(path_destination) == False:
		os.mkdir(path_destination)
	# Unpack files
	os.system('tar -xzf '+version_ID +' -C '+ path_destination)

def identify_master_tex_file(path,arxiv_ID):
	tex_files = []
	for file in os.listdir(path):
		if file.endswith(".tex") and file.startswith(arxiv_ID) == False:
			tex_files.append(file)
	if len(tex_files) == 1:
		master_file = tex_files[0]
	else:
		for file in tex_files:
			with open(path+file) as f:
				if 'begin{document}' in f.read():
					master_file = file
					break
		else:
			print("Error in identify_master_tex_file(): Among the ",len(tex_files)," tex files, no master file could be identified.")
			os.abort()
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
		# tex_file = identify_master_tex_file(path,arxiv_ID)
		# os.chdir(path)
		# os.system("pdflatex -interaction=batchmode "+tex_file)
		# os.system("bibtex " + os.path.splitext(tex_file)[0])
		# os.chdir("..")
		# bbl_file = os.path.splitext(tex_file)[0]+".bbl"
	print("Bibliography file in",path,":\t",bbl_file)
	return bbl_file

def remove_temporary_files(arxiv_ID):
	print("Delete temporary files:")
	for file in os.listdir("."):
		if file.startswith(".temp_"+arxiv_ID) or (file.startswith(arxiv_ID) and not file.endswith("pdf")):
			print("\t",file)
			os.system("rm -r "+ file)

def print_title(ID,v1,v2):
	asci_title = "                                    __  ___       \n  ___ ___  _ __ ___  _ __   __ _ _ _\ \/ (_)_   __\n / __/ _ \| '_ ` _ \| '_ \ / _` | '__\  /| \ \ / /\n| (_| (_) | | | | | | |_) | (_| | |  /  \| |\ V / \n \___\___/|_| |_| |_| .__/ \__,_|_| /_/\_\_| \_/  \n                    |_|                           \n"
	print(asci_title)
	print("Version ",version,", developed by",author,"("+year+")")
	print("Compare [arXiv:"+ID+"]: v"+str(v1)+" vs v"+str(v2),"\n")

if __name__ == "__main__":
	arxiv_ID = str(sys.argv[1])
	version_a = sys.argv[2]
	version_b = sys.argv[3]
	compare_preprints(arxiv_ID,version_a,version_b)