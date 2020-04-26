import os
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import pandas as pd
import re

base_dir = "/data/Applications/GitScript/Covid19/NextStrainFiles/" 

gisaid_metadata = os.path.join(base_dir,"data/original/data/metadata.tsv") 
lspq_sgil_extract = os.path.join(base_dir,"data/sgil_extract.tsv")

gisaid_sequences = os.path.join(base_dir,"data/gisaid/randomseq.fasta")
lspq_sequences = os.path.join(base_dir,"data/lspq/sequences.fasta")

df_lspq = pd.read_csv(lspq_sgil_extract,delimiter="\t",index_col=False)
df_gisaid = pd.read_csv(gisaid_metadata,delimiter="\t",index_col=False)

test =df_lspq[df_lspq['NO_LSPQ'].isin(['L00251524','Lkkk00251535'])]

rec_id_list = []

for rec in SeqIO.parse(gisaid_sequences,'fasta'):
    seqid = re.search(r'^\S+\/(\S+\/\S+\/\d{4})\|\S+',rec.id).group(1)
    rec_id_list.append(seqid)


for rec in SeqIO.parse(lspq_sequences,'fasta'):
    seqid = re.search(r'(^\S+)\/\S+\/\S+',rec.id).group(1)
    rec_id_list.append(seqid)


subset_lspq = df_lspq[df_lspq['NO_LSPQ'].isin(rec_id_list)]
print(subset_lspq)

subset_gisaid = df_gisaid[df_gisaid['strain'].isin(rec_id_list)]
print(subset_gisaid)
