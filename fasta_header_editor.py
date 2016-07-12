#!/bin/python
# Chad Smith 2016-07-12
import sys
import string
import argparse

def count(args):
	file=open(args.fasta,'r')
	for line in file:
	    if '>' in line:
                if args.genbank is True:
                # Delete everything in Genbank header but accession and description
	            split=line.split('|')
	            line='>'+split[3]+split[4]
                # Find and replace.
                if args.pattern is not None:
                        for i in args.pattern:
	        	    line=line.replace(i,"")
                if args.replace is not None:
                    line=line.replace(args.replace[0],args.replace[1])
                sys.stdout.write(line)
	    else:
	        sys.stdout.write(line)
        file.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Edits header of Genbank FASTA files')
	parser.add_argument('fasta',type=str)
	parser.add_argument('--delete', dest='pattern', nargs='+', help='Pattern(s) to delete')
	parser.add_argument('--replace', nargs=2, help='Replace first argument with the second')
	parser.add_argument('--genbank', action='store_true',help='Reformats Genbank header if present')
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit()
	args = parser.parse_args()
	count(args)
