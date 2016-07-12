#!/bin/python
# Chad Smith 7/9/2016
import sys
import argparse
import csv
from Bio import SeqIO
from Bio.SeqFeature import SeqFeature

def index_genbank_features(gb_record, feature_type, qualifier) :
    answer = dict()
    for (index, feature) in enumerate(gb_record.features) :
        if feature.type==feature_type :
            if qualifier in feature.qualifiers :
                #There should only be one locus_tag per feature, but there
                #are usually several db_xref entries
                for value in feature.qualifiers[qualifier] :
                    if value in answer :
                        print "WARNING - Duplicate key %s for %s features %i and %i" \
                           % (value, feature_type, answer[value], index)
                    else :
                        answer[value] = index
    return answer


def count(args):
    gb=args.gb
    output=[]
    for arg in args.gb:
        records=SeqIO.parse(arg,"genbank")
	for record in records:
		organism=record.annotations["organism"]
		host_dict=index_genbank_features(record,"source","host")
		if not host_dict: host=""
		else:
			for key, value in host_dict.items(): host=key
		isolation_dict=index_genbank_features(record,"source","isolation_source")
		if not isolation_dict: isolation="not specificed"
		else: 
			for key, value in isolation_dict.items(): isolation=key
		seqlen=len(record.seq)
		output.append("%s,%s,%s,%s,%i\n" % (record.id,organism,host,isolation,seqlen))
        if args.filename == '-': 
            for i in output: 
                out=i.strip('\n')
	        print out
        else:
            out_handle=open(args.filename,'w')
            for i in output: out_handle.write(i)
            out_handle.close()

if __name__ == '__main__':
        parser = argparse.ArgumentParser(description='Parse Genbank GB files to stdout')
        parser.add_argument('gb', nargs='+',help='Genbank flat file(s)')
        parser.add_argument('--out', dest='filename',default="-",help='CSV output file')

        if len(sys.argv)==1:
                parser.print_help()
                sys.exit()
        args = parser.parse_args()
        count(args)

