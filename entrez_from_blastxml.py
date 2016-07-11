#!/bin/python
# Chad Smith 07/09/16
import sys
import os
import numpy
from Bio import SeqIO
from Bio import Entrez
from Bio.Blast import NCBIXML
def unique(seq): # Dave Kirby
    # Order preserving
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]

if len(sys.argv) == 1 :
    print "usage: ", sys.argv[0], " <blast xml>"
    print "Parses a BLAST xml file and retrieves Genbank flat files."
    exit(1)
for xml in sys.argv[1:]:
        result_handle = open(xml)
	blast_records = NCBIXML.parse(result_handle)

	# Parse accessions from xml
	accessions=[]
	for rec in blast_records:
		for alignment in rec.alignments:
			for hsp in alignment.hsps:
				accessions.append(alignment.accession)
	accessions=unique(accessions)
	
	# Set file name
	prefix=str.split(xml,'.')
	filename=prefix[0]+".gb"
	out_handle = open(filename, "w")
	
	# Write entrez gb
	Entrez.email = "chad.smith123@gmail.com"
        print "Retrieving Entrez gb from",xml
	for i in accessions:
		net_handle=Entrez.efetch(db="nucleotide", id=i, rettype="gb", retmode="text")
		out_handle.write(net_handle.read())
	out_handle.close()
	net_handle.close()
