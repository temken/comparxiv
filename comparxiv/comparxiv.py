#!/usr/bin/env python

import os
import sys
import requests

from sys import platform
from tqdm import tqdm

version = '0.1.4'
author = 'Timon Emken'
year = '2020'

temp_folder = ".temp_comparxiv/"
def compare_preprints(arxiv_ID, version_a, version_b,keep_temp,show_latex_output,dont_open_pdf,dont_compare_equations):

	#Check if old or new arxiv ID
	if "/" in arxiv_ID:
		ID_a = os.path.split(arxiv_ID)[-1]+"v"+str(version_a)
		ID_b = os.path.split(arxiv_ID)[-1]+"v"+str(version_b)
	else:
		ID_a = arxiv_ID+"v"+str(version_a)
		ID_b = arxiv_ID+"v"+str(version_b)

	#Create folder for temporary files
	if os.path.exists(temp_folder) == False:
		os.mkdir(temp_folder)

	temp_folder_a = './' + temp_folder + 'temp_' + ID_a+'/'
	temp_folder_b = './' + temp_folder + 'temp_' + ID_b+'/'
	diff_file = os.path.split(arxiv_ID)[-1]+"_v"+str(version_a)+"v"+str(version_b)

	# #1. Download and unpack files
	download_from_arxiv(arxiv_ID,version_a)
	download_from_arxiv(arxiv_ID,version_b)
	unpack_source_files(arxiv_ID,version_a,temp_folder_a)
	unpack_source_files(arxiv_ID,version_b,temp_folder_b)

	#2. Identify the .tex and .bbl files.
	#2.1 tex files
	master_file_a = identify_master_tex_file(temp_folder_a,arxiv_ID)
	master_file_b = identify_master_tex_file(temp_folder_b,arxiv_ID)
	#2.2 bbl files
	bbl_file_a = identify_bbl_file(temp_folder_a,arxiv_ID)
	bbl_file_b = identify_bbl_file(temp_folder_b,arxiv_ID)

	#3. Latexdiff
	#3.1 tex files 
	print("Run latexdiff on .tex files:")
	print("\t",temp_folder_a+master_file_a)
	print("\t",temp_folder_b+master_file_b)

	latexdiff_command_tex = "latexdiff "
	if show_latex_output == False:
		latexdiff_command_tex += "--ignore-warnings "
	if dont_compare_equations:
		latexdiff_command_tex += "--math-markup=0 "
	
	latexdiff_command_tex += temp_folder_a+master_file_a+" "+temp_folder_b+master_file_b+">"+temp_folder_b+diff_file+".tex"

	os.system(latexdiff_command_tex)

	#3.2 Try to run latexdiff on bbl.
	if bbl_file_a != None and bbl_file_b != None:
		print("\nRun latexdiff on .bbl files:")
		print("\t",temp_folder_a+bbl_file_a)
		print("\t",temp_folder_b+bbl_file_b)
		if show_latex_output == False:
			latexdiff_command_bbl = "latexdiff --ignore-warnings "+temp_folder_a+bbl_file_a+" "+temp_folder_b+bbl_file_b+">"+temp_folder_b+diff_file+".bbl"
		else:
			latexdiff_command_bbl = "latexdiff "+temp_folder_a+bbl_file_a+" "+temp_folder_b+bbl_file_b+">"+temp_folder_b+diff_file+".bbl"
		os.system(latexdiff_command_bbl)

	#4. Run pdflatex
	Generate_PDF(diff_file,temp_folder_b,show_latex_output)

	#5. If unsuccessful, try again with a copy of the version b .bbl file.
	if bbl_file_b != None and os.path.isfile(temp_folder_b+diff_file+".pdf") == False:
		print("\nCopy the .bbl file of version b.")
		os.system("cp "+ temp_folder_b + bbl_file_b + " " + temp_folder_b + diff_file+".bbl")
		Generate_PDF(diff_file,temp_folder_b,show_latex_output)
	
	success = False;
	if os.path.isfile(temp_folder_b+diff_file+".pdf"):
		success = True
	#6. Compare figures
	# todo

	#7. If successful copy the .pdf.
	if success:
		os.system("mv " +temp_folder_b+diff_file+".pdf" + " ./" + diff_file+".pdf")
		print("\nFinished: success.")
		if dont_open_pdf == False:
			if platform == "linux" or platform == "linux2":
				os.system("xdg-open "+diff_file+".pdf")
			elif platform == "darwin":
				os.system("open "+diff_file+".pdf")
	else:
		print("\nFinished: failure. No pdf file could be generated.\nTroubleshooting:")
		print("\t1.) To see more terminal output run:\n\t\t'comparxiv --show_latex_output "+arxiv_ID+" "+str(version_a)+" " + str(version_b) +"'")
		print("\t2.) In some cases latex math environments cause problems with latexdiff. Try running:\n\t\t'comparxiv --dont_compare_equations "+arxiv_ID+" "+str(version_a)+" " + str(version_b) +"'")
	
	#8. Delete temporary files
	if keep_temp == False:
		remove_temporary_files(ID_a)

	return success

def Generate_PDF(file, folder, show_latex_output):
	os.chdir(folder)
	pdflatex_command = "pdflatex -interaction=nonstopmode "+file+".tex"
	if show_latex_output == False:
		pdflatex_command += " 2>&1 > /dev/null"
	print("Compile .tex file via")
	print("\t",pdflatex_command,"\n")
	os.system(pdflatex_command)
	os.system(pdflatex_command)
	os.chdir("../..")


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
		filepath = "./"+temp_folder+os.path.split(arxiv_ID)[-1]+"v"+str(version)
		
	else:
		filepath = "./"+temp_folder+arxiv_ID+"v"+str(version)

	if os.path.isfile(filepath) == False:
		url="https://arxiv.org/e-print/"+arxiv_ID+"v"+str(version)
		download_from_url(url,filepath)
	else:
		print("Download of source files for "+arxiv_ID+"v"+str(version)+" not necessary.")

#Unpack the archived files to a temporary folder
def unpack_source_files(arxiv_ID,version,path_destination):
	version_ID = arxiv_ID+"v"+str(version)
	#Check if old or new arxiv ID
	if "/" in arxiv_ID:
		path_source = "./"+temp_folder+os.path.split(version_ID)[-1]
	else:
		path_source = "./"+temp_folder+version_ID

	print(path_destination,path_source)

	# Create folder for temporary files
	print("Unpack source files of",version_ID,"to",path_destination,".")
	if os.path.isfile(path_source) and os.path.exists(path_destination) == False:
		os.makedirs(path_destination)
	# Unpack files
	os.system('tar -xzf '+path_source +' -C '+ path_destination)

def identify_master_tex_file(path,arxiv_ID):
	tex_files = []
	for file in os.listdir(path):
		if file.endswith(".tex") and (file.startswith(arxiv_ID) or file.startswith(os.path.split(arxiv_ID)[-1]))== False:
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
			print("Bibliography (.bbl) file in",path,":\t",bbl_file)
			break
	# Possibility b: No .bbl file exists.
	else:
		bbl_file = None
		print("No .bbl file found in\t",path)
	return bbl_file

def remove_temporary_files(arxiv_ID):
	os.system("rm -r "+ temp_folder)

def print_title(ID,v1,v2):
	asci_title = "                                    __  ___       \n  ___ ___  _ __ ___  _ __   __ _ _ _\ \/ (_)_   __\n / __/ _ \| '_ ` _ \| '_ \ / _` | '__\  /| \ \ / /\n| (_| (_) | | | | | | |_) | (_| | |  /  \| |\ V / \n \___\___/|_| |_| |_| .__/ \__,_|_| /_/\_\_| \_/  \n                    |_|                           \n"
	print(asci_title)
	print("Version ",version,", developed by",author,"("+year+")")
	print("\nCompare [arXiv:"+ID+"]: v"+str(v1)+" vs v"+str(v2),"\n")

if __name__ == "__main__":
	arxiv_ID = str(sys.argv[1])
	version_a = sys.argv[2]
	version_b = sys.argv[3]
	compare_preprints(arxiv_ID,version_a,version_b)