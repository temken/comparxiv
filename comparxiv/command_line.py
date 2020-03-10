import comparxiv
import sys

def main():
	arxiv_ID = str(sys.argv[1])
	version_a = sys.argv[2]
	version_b = sys.argv[3]
	# comparxiv.print_title(arxiv_ID,version_a,version_b)
	comparxiv.compare_preprints(arxiv_ID,version_a,version_b)