import comparxiv
import sys
import argparse

def main():
	parser = argparse.ArgumentParser(description="Comparxiv v" + comparxiv.version + ", developed by " + comparxiv.author + " ("+ comparxiv.year + ") - Compare two versions of an arXiv preprint.")
	parser.add_argument("-T","--keep_temp_files", help="Do not delete temporary files in the end.",
                    action="store_true")
	parser.add_argument("-L","--show_latex_output", help="Show the terminal output of pdflatex.",
                    action="store_true")
	parser.add_argument("-P","--dont_open_pdf", help="Do not automatically open the generated pdf in the end.",
                    action="store_true")
	parser.add_argument("-E","--dont_compare_equations", help="Run latexdiff with the flag --math-markup=0.",
                    action="store_true")
	parser.add_argument("arxiv_ID", help = "The arXiv ID of the paper to be compared, e.g. \'1905.06348\'.",
						type = check_arxiv_ID)
	parser.add_argument("version_A", help = "The reference version of the preprint to be compared. (Default: second latest version)",
						nargs='?', type = check_version_input)
	parser.add_argument("version_B", help = "The new version of the preprint to be compared. (Default: latest version)",
						nargs='?', type = check_version_input)
	args = parser.parse_args()

	if args.version_A is not None and args.version_A == args.version_B:
		raise argparse.ArgumentTypeError("Versions to compare are identical.")

	interpret_arguments(args)

	comparxiv.compare_preprints(args.arxiv_ID,args.version_A,args.version_B,args.keep_temp_files,args.show_latex_output,args.dont_open_pdf,args.dont_compare_equations)

def check_version_input(value):
	try:
		ivalue = int(value)
	except ValueError:
		raise argparse.ArgumentTypeError("Version %s is an invalid arXiv version." % value)
	if ivalue < 1:
		raise argparse.ArgumentTypeError("Version %s is an invalid arXiv version." % value)
	return ivalue

def check_arxiv_ID(ID):
	is_valid_ID = False
	# New IDs
	if len(ID) > 6 and ID[4] == "." and ID.split(".",1)[0].isdigit() and int(ID[2:4])<13 and ID[-1].isdigit():
		is_valid_ID = True
	# Old IDs
	elif "/" in ID:
		i = ID.find("/")
		if ID[i+3:i+5].isdigit() and int(ID[i+3:i+5]) < 13 and ID[-1].isdigit():
			is_valid_ID = True
	if is_valid_ID:
		return ID
	else:
		raise argparse.ArgumentTypeError("The input %s is not a valid arXiv ID." % ID)

def interpret_arguments(args):
	#1. The user might have specified a version N in the ID. Then compare N-1 to N
	if "v" in args.arxiv_ID:
		user_given_version = int(args.arxiv_ID.split("v",1)[1])
		args.arxiv_ID = args.arxiv_ID.split("v",1)[0]
		if args.version_A == None:
			if user_given_version == 1:
				args.version_A = 1
				args.version_B = 2
			elif user_given_version > 1:
				args.version_A = user_given_version-1
				args.version_B = user_given_version
		else:
			args.version_B = args.version_A
			args.version_A = user_given_version


	#2. For one given version, the comparison should be to the previous version
	elif args.version_A is not None and args.version_B is None:
		if args.version_A < 2:
			args.version_A = 1
			args.version_B = 2
		else:
			args.version_B = args.version_A
			args.version_A -= 1

	#3. Without given version, the comparison should be between the two most recent versions.
	elif args.version_A is None and args.version_B is None:
		latest_version = comparxiv.latest_available_version(args.arxiv_ID)
		args.version_A = latest_version -1
		args.version_B = latest_version