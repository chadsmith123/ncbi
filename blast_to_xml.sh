#!/bin/bash -x
# Blast Search to XML
# Chad Smith 07/09/2016
# Executes a BLAST search and returns a XML file. 
# Requires blastxml_to_tab.py

BLASTXML_TO_TAB=blastxml_to_tab.py
NUM_ALIGNMENTS=10
EVALUE=1e-10
#PERC_IDENTITY=97
#ENTREZ_QUERY="gut or feces or fecal or intestine or foregut or midgut or hindgut or ileum or rectum or colon or cecum or jejunum or duodenum"

if [ -z $1 ]; then
    echo "usage: $0 <FASTA>"
    echo "Writes an xml file from a blast search."
    exit
fi

for i in $@; do 
	#prefix=`echo $i|cut -f1 -d '.'`
	prefix=`basename $i|cut -f1 -d '.'`
	echo "Blasting $i"
	blastn -query $i -db nt -remote\
	-evalue $EVALUE\
	-num_alignments $NUM_ALIGNMENTS\
	-export_search_strategy ${prefix}_blast.asn\
	-outfmt 5\
	-out ${prefix}_blast.xml
       	#-entrez_query "$ENTREZ_QUERY"\
	#-outfmt "6 sallseqid salltitles qseqid evalue pident bitscore"
	#-perc_identity $PERC_IDENTITY\
	python $BLASTXML_TO_TAB ${prefix}_blast.xml > ${prefix}_blast.tab
done
# Use custom outfmt 
	#blastn -query $i -db nt -perc_identity 0.97 -evalue 1e-10 -remote -num_alignments $NUM_ALIGNMENTS -entrez_query "gut or feces or intestine or foregut or midgut or hindgut or ileum or rectum or colon or cecum or jejunum or duodenum" -outfmt "6 sallseqid salltitles qseqid evalue bitscore" -out ${prefix}.xml;done
