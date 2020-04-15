"""
Eric Fournier 20200415
"""

import os
import sys
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import random
import logging

logging.basicConfig(level = logging.DEBUG)


class SeqReader(object):
    def __init__(self,fasta_in):
        pass
        self.fasta_in = fasta_in
        self.rec_list_in = []
        self.rec_list_out = []
        self.nb_rec_in = 0

    def Flush(self):
        self.rec_list_in = []
        self.rec_list_out = []

    def BuildRecListIn(self):
        for rec in SeqIO.parse(self.fasta_in,'fasta'):
            self.rec_list_in.append(rec)
            self.nb_rec_in += 1

    def BuildRecListOut(self, nb_rec, homogeneous):
        self.BuildRecListIn()

        if nb_rec > self.nb_rec_in:
            logging.error("Le nombre de sequences choisie est trop grand")
            sys.exit(0)
        
        if not homogeneous:
            for i in range(1,nb_rec + 1):
                rec = SeqRecord(seq = self.rec_list_in[i].seq, id = "Seq_" + str(i), description = "")
                self.rec_list_out.append(rec)
        else:
            single_rec = self.rec_list_in[0]
            for i in range(1, nb_rec + 1): 
                rec = SeqRecord(seq = single_rec.seq, id = "Seq_" + str(i), description = "")
                self.rec_list_out.append(rec) 

class SeqWriter(object):
    def __init__(self,seq_reader):
        self.fasta_out = ""
        self.seq_reader = seq_reader

    def CreateFastaOut(self,fasta_out,nb_seq,homogeneous = False):
        self.fasta_out = fasta_out
        self.seq_reader.Flush()

        self.seq_reader.BuildRecListOut(nb_seq,homogeneous)       
         
        SeqIO.write(self.seq_reader.rec_list_out, self.fasta_out,'fasta')


def CreateFastaCovid(fasta_in_file,fasta_out_file,nb_seq,homogeneous):

    seq_reader = SeqReader(fasta_in_file)
    seq_writer = SeqWriter(seq_reader)

    seq_writer.CreateFastaOut(fasta_out_file,nb_seq,homogeneous)

