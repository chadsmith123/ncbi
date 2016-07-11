#!/bin/python
# Chad Smith 07/09/2016
import sys
from Bio import SeqIO

if len(sys.argv) != 3:
    print "usage: ", sys.argv[0], "<accessions list> <genbank gb>"
    print "Writes a fasta file from a Genbank file using a list of accessions."
    exit(1)

# Create a list of accessions from input file
file=open(sys.argv[1],'r')
file_ac=file.readlines()
accessions=map(str.rstrip,file_ac)

# Extract accessions from a Genbank flat file
records=[]
for seq_record in SeqIO.parse(sys.argv[2],"genbank"):
    if seq_record.name in accessions:
        records.append(seq_record)
SeqIO.write(records,sys.stdout,"fasta")
