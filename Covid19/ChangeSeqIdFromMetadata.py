"""
Eric Fournier 20200415
"""

import os
import sys
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import random
import logging

basedir = "/data/PROJETS/COVID_19/TestMetadata"

metadata = os.path.join(basedir,"metadata.tsv")
metadata_handle = open(metadata)
metadata_handle.readline()

fake_seq_file = os.path.join(basedir,"sequences_fakeid.fasta")
new_seq_file = os.path.join(basedir,"sequences.fasta")

new_rec_list = []

logging.basicConfig(level = logging.DEBUG)

metadata_id = []

for line in metadata_handle:
    #print(line)
    id = line.split("\t")[0]
    metadata_id.append(id)

#print(str(metadata_id))

metadata_handle.close()

inc = 0

for rec in SeqIO.parse(fake_seq_file,'fasta'):
    #print(rec.id)
    new_rec = SeqRecord(seq = rec.seq, id = metadata_id[inc], description = "" )
    inc += 1
    new_rec_list.append(new_rec)

SeqIO.write(new_rec_list,new_seq_file,"fasta")

logging.info("End")

