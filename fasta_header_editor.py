#!/bin/python
# Chad Smith 2016-07-12
import sys
import re
import string
import argparse

def count(args):
        if args.fasta is not '-':
            file=open(args.fasta,'r')
        else:
            file=sys.stdin
	for line in file:
	    if '>' in line:
                if args.genbank is True:
                # Delete everything in Genbank header but accession and description
	            split=line.split('|')
	            line='>'+split[3]+split[4]
                # Find and replace.
                if args.pattern is not None:
                        for i in args.pattern:
	        	    line=re.sub(i,"",line)
                if args.replace is not None:
                    line=re.sub(args.replace[0],args.replace[1],line)
                sys.stdout.write(line)
	    else:
	        sys.stdout.write(line)
        file.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Edits header of Genbank FASTA files')
	parser.add_argument('--delete', dest='pattern', nargs='+', help='Pattern(s) to delete')
	parser.add_argument('--replace', nargs=2, help='Replace first argument with the second')
	parser.add_argument('--genbank', action='store_true',help='Reformats Genbank header if present')
	parser.add_argument('fasta',type=str)
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit()
	args = parser.parse_args()
	count(args)
