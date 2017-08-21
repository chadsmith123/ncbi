#!/usr/bin/env python
"""
ENTREZ Search
Author: Chad Smith 

Searches Genbank for <pattern> and returns output.
Requires Biopython
"""

import sys
import argparse
from Bio import SeqIO
from Bio import Entrez
from urllib.request import HTTPError
import time

def count(args):
	Entrez.email = "chad.smith123@gmail.com"
	# Count the number of records if --count is given.
	if args.count is True and args.db != 'genome':
		handle = Entrez.esearch(db=args.db, term=args.pattern,rettype='count')
		records = Entrez.read(handle)
		print(records['Count'] + ' hits for ' + args.pattern)
		exit(1)	
	# Collect accession numbers
	handle = Entrez.esearch(db=args.db, term=args.pattern,retmax=args.num,sort='relevance')
	records = Entrez.read(handle)
	accessions=records["IdList"]
	if args.db == 'genome':
		# Retrieve uiids from nuccore for genomes
		link = Entrez.elink(dbfrom='genome', db='nuccore', id=accessions)
		linkr = Entrez.read(link)
		linkr_dict = linkr[0]['LinkSetDb'][0]['Link']
		uiid = [list(x.values())[0] for x in linkr_dict]
		# Retrieve accessions ('captions') from esummary output 
		captions = []
		for item in uiid:
                        handle_uiid = Entrez.esummary(db='nuccore', id=item)
                        record_uiid = Entrez.read(handle_uiid)
                        captions.append(record_uiid[0]['Caption'])
		if args.pattern2 != None:
			args.pattern = args.pattern + ' AND ' + args.pattern2
		# Collate pattern and retrieve filtered accessions from nuccore
		pattern = ' OR '.join([d + "[Accession]" for d in captions]) 
		pattern = '(' + pattern + ')' + ' AND ' + args.pattern 
		handle_pattern = Entrez.esearch(db='nuccore', term=pattern, retmax=args.num, sort='relevance')
		records_pattern = Entrez.read(handle_pattern)
		accessions = records_pattern["IdList"]
		if args.count is True:
			print(str(len(accessions)) + ' hits for ' + args.pattern)
			exit(1)
			
	# Fetch entrez output and write to stdout
	for i in accessions:
		try:
			net_handle=Entrez.efetch(db='nuccore', id=i, rettype=args.rettype, retmode="text")
		except HTTPError:
			time.sleep(20)
			net_handle=Entrez.efetch(db='nuccore', id=i, rettype=args.rettype, retmode="text")
		if args.descr is True:
			record = SeqIO.read(net_handle, "fasta")
			print(record.description)
		else:
			print(net_handle.read())

	
if __name__ == '__main__':
        parser = argparse.ArgumentParser(description='Search genbank and returns flat files')
        parser.add_argument('-pattern', dest='pattern', type=str, help='Search pattern')
        parser.add_argument('-pattern2', dest='pattern2', type=str, help='Search pattern for genome database')
        parser.add_argument('-n', dest='num', default='20', type=int, help='Number of records to return')
        parser.add_argument('-db', dest='db', default='nucleotide', type=str, help='NCBI database')
        parser.add_argument('-rettype', dest='rettype', default='fasta', type=str, help='Return type', choices=['fasta', 'gb'])
        parser.add_argument('--count', action='store_true',help='Return number of records and exit')
        parser.add_argument('--descr', action='store_true',help='Return sequence description')
        if len(sys.argv)==1:
                parser.print_help()
                sys.exit()
        args = parser.parse_args()
        count(args)

# Code to write a file instead of stdout.
    #out_handle.write(net_handle.read())
