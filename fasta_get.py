#!/usr/bin/env python
"""
FASTA Get from Genbank
Chad Smith 07/11/2016

Retrieves FASTA from genbank using accessions from stdin (-) or in a file.
Requires: Biopython
"""
import sys
from Bio import Entrez
from Bio import SeqIO
from urllib.request import HTTPError
import time

if len(sys.argv) ==1 :
    print("usage: ", sys.argv[0], "<accessions file>")
    print("Extracts FASTA for a list of accessions in <file> or stdin (-)")
    exit(1)

Entrez.email ="chad.smith123@gmail.com"
if sys.argv[1] == '-':
    f=[]
    for i in sys.stdin:
        f.append(i)
else:
    f = open(sys.argv[1])

for line in iter(f):
	try:
        	handle = Entrez.efetch(db="nucleotide", id=line, retmode="text",rettype="fasta")
	except HTTPError:
        	time.sleep(20)
        	handle = Entrez.efetch(db="nucleotide", id=line, retmode="text",rettype="fasta")
	record = SeqIO.read(handle,"fasta")
	print(">"+record.description)
	print(record.seq)
if sys.argv[1] != '-':
    f.close()
