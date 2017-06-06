#!/bin/python
"""
ENTREZ Search
Chad Smith 07/11/16

Searches Genbank for <pattern> and returns a flat file. 
Requires Biopython
"""

import sys
import argparse
from Bio import Entrez

def count(args):

	Entrez.email = "chad.smith123@gmail.com"
	# Count the number of records if --count is given.
	if args.count is True:
		handle = Entrez.esearch(db="nucleotide", term=args.pattern,rettype='count')
		records = Entrez.read(handle)
		print(records)
		exit(1)	

	# Collect accession numbers
	handle = Entrez.esearch(db="nucleotide", term=args.pattern,retmax=args.num,sort='relevance')
	records = Entrez.read(handle)
	accessions=records["IdList"]

	# Fetch entrez gb and write to stdout
	for i in accessions:
	    net_handle=Entrez.efetch(db="nucleotide", id=i, rettype="gb", retmode="text")
	    print(net_handle.read())
	
if __name__ == '__main__':
        parser = argparse.ArgumentParser(description='Search genbank and returns flat files')
        parser.add_argument('-pattern', dest='pattern', type=str, help='Search pattern')
        parser.add_argument('-n', dest='num', default='20', type=int, help='Number of records to return')
        parser.add_argument('--count', action='store_true',help='Return number of records and exit')
        if len(sys.argv)==1:
                parser.print_help()
                sys.exit()
        args = parser.parse_args()
        count(args)

# Code to write a file instead of stdout.
    #out_handle.write(net_handle.read())
    #out_handle.close()
#net_handle.close()

	
