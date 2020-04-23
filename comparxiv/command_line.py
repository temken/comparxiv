import comparxiv
import sys
import argparse

def main():
	parser = argparse.ArgumentParser(description="Comparxiv v" + comparxiv.version + ", developed by " + comparxiv.author + " ("+ comparxiv.year + ") - Compare two versions of an arXiv preprint.")
	parser.add_argument("-T","--keep_temp_files", help="Do not delete temporary files in the end.",
                    action="store_true")
	parser.add_argument("-L","--show_pdflatex_output", help="Show the terminal output of pdflatex.",
                    action="store_true")
	parser.add_argument("-P","--dont_open_pdf", help="Do not automatically open the generated pdf in the end.",
                    action="store_true")
	parser.add_argument("arxiv_ID", help = "The arXiv ID of the paper to be compared, e.g. \'1905.06348\'.",
						type = str)
	parser.add_argument("version_A", help = "The reference version of the preprint to be compared. (Default: 1)",
						nargs='?', default = 1, type = check_version_input)
	parser.add_argument("version_B", help = "The new version of the preprint to be compared. (Default: 2)",
						nargs='?', default = 2, type = check_version_input)
	args = parser.parse_args()
	comparxiv.print_title(args.arxiv_ID,args.version_A,args.version_B)
	comparxiv.compare_preprints(args.arxiv_ID,args.version_A,args.version_B,args.keep_temp_files,args.show_pdflatex_output,args.dont_open_pdf)

def check_version_input(value):
	try:
		ivalue = int(value)
	except ValueError:
		raise argparse.ArgumentTypeError("Version %s is an invalid arXiv version." % value)
	if ivalue < 1:
		raise argparse.ArgumentTypeError("Version %s is an invalid arXiv version." % value)
	return ivalue