#!/bin/python
# Chad Smith 7/9/2016
import sys
import csv
from Bio import SeqIO
from Bio.SeqFeature import SeqFeature
if len(sys.argv) ==1 :
    print "usage: ", sys.argv[0], " <genbank db>"
    print "Parses metadata from Genbank flat files."
    exit(1)


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

for arg in sys.argv[1:]:
        records=SeqIO.parse(arg,"genbank")
        #record.annotations.keys()
	prefix=str.split(arg,'.')
        filename=prefix[0]+".csv"
        print "Writing",filename
	out_handle=open(filename,"w")
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
		output="%s,%s,%s,%s,%i\n" % (record.id,organism,host,isolation,seqlen)
                out_handle.write(output)
        out_handle.close()
