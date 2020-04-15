import os
#import Bio
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import random
#from Bio.Seq import MutableSeq
import logging

logging.basicConfig(level = logging.DEBUG)


#TODO max selon nb seq in

fasta_in_file =  os.path.join(os.path.dirname(os.getcwd()),"data/gisaid_covid19_usa_1759.fasta")
fasta_in_file_test =  os.path.join(os.path.dirname(os.getcwd()),"data/three_seq.fasta")
fasta_out_10seq_homogeneous =  os.path.join(os.path.dirname(os.getcwd()),"data/covid19_10seq_homogeneous.fasta")
fasta_out_200seq_heterogeneous =  os.path.join(os.path.dirname(os.getcwd()),"data/covid19_200seq_heterogeneous.fasta")
fasta_out_10seq_heterogeneous =  os.path.join(os.path.dirname(os.getcwd()),"data/covid19_10seq_heterogeneous.fasta")


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
        if not homogeneous:
            for i in range(1,nb_rec+1):
                rec = SeqRecord(seq = self.rec_list_in[i].seq, id = "Seq_" + str(i), description = "")
                self.rec_list_out.append(rec)
        else:
            pass
 
class SeqWriter(object):
    def __init__(self,seq_reader):
        self.fasta_out = ""
        self.seq_reader = seq_reader

    def CreateFastaOut(self,fasta_out,nb_seq,homogeneous = False):
        self.fasta_out = fasta_out
        self.seq_reader.Flush()

        self.seq_reader.BuildRecListOut(nb_seq,homogeneous)        
        SeqIO.write(self.seq_reader.rec_list_out, self.fasta_out,'fasta')


seq_reader = SeqReader(fasta_in_file_test)
seq_writer = SeqWriter(seq_reader)

seq_writer.CreateFastaOut(fasta_out_10seq_heterogeneous,2,False)
