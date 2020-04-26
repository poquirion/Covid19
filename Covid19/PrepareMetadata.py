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

out_metadata = os.path.join(base_dir,"data/metadata.tsv")
out_sequences = os.path.join(base_dir,"data/sequences.fasta")

for rec in SeqIO.parse(gisaid_sequences,'fasta'):
    seqid = re.search(r'^\S+\/(\S+\/\S+\/\d{4})\|\S+',rec.id).group(1)
    rec_id_list.append(seqid)


for rec in SeqIO.parse(lspq_sequences,'fasta'):
    seqid = re.search(r'(^\S+)\/\S+\/\S+',rec.id).group(1)
    rec_id_list.append(seqid)


subset_lspq = df_lspq[df_lspq['NO_LSPQ'].isin(rec_id_list)]
subset_gisaid = df_gisaid[df_gisaid['strain'].isin(rec_id_list)]

#subset_lspq_subcol = subset_lspq[['NO_LSPQ','DATE_PRELEV','SEX','AGE','RSS_PATIENT','POSTAL_CODE','VOYAGE_PAYS_1']] this create a view https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
subset_lspq_subcol = subset_lspq.loc[:,('NO_LSPQ','DATE_PRELEV','SEX','AGE','RSS_PATIENT','POSTAL_CODE','VOYAGE_PAYS_1')] # this create a copy
subset_lspq_subcol.columns = ['strain','date','sex','age','rss','rta','voyage']
subset_lspq_subcol.insert(loc=1,column='virus',value='ncov',allow_duplicates=True)
subset_lspq_subcol.insert(loc=5,column='country',value='Canada',allow_duplicates=True)
subset_lspq_subcol.insert(loc=6,column='division',value='Quebec',allow_duplicates=True)
subset_lspq_subcol.insert(loc=9,column='country_exposure',value='',allow_duplicates=True)
subset_lspq_subcol.insert(loc=10,column='division_exposure',value='',allow_duplicates=True)
subset_lspq_subcol.insert(loc=11,column='rss_exposure',value='',allow_duplicates=True)
subset_lspq_subcol.insert(loc=12,column='rta_exposure',value='',allow_duplicates=True)
subset_lspq_subcol.loc[subset_lspq_subcol.voyage == 'AUCUN_VOYAGE','country_exposure'] = subset_lspq_subcol.country
subset_lspq_subcol.loc[subset_lspq_subcol.voyage == 'AUCUN_VOYAGE','division_exposure'] = subset_lspq_subcol.division
subset_lspq_subcol.loc[subset_lspq_subcol.voyage == 'AUCUN_VOYAGE','rss_exposure'] = subset_lspq_subcol.rss
subset_lspq_subcol.loc[subset_lspq_subcol.voyage == 'AUCUN_VOYAGE','rta_exposure'] = subset_lspq_subcol.rta
subset_lspq_subcol.loc[subset_lspq_subcol.voyage != 'AUCUN_VOYAGE','country_exposure'] = subset_lspq_subcol.voyage
subset_lspq_subcol.loc[subset_lspq_subcol.voyage != 'AUCUN_VOYAGE','division_exposure'] = subset_lspq_subcol.voyage
subset_lspq_subcol.loc[subset_lspq_subcol.voyage != 'AUCUN_VOYAGE','rss_exposure'] = subset_lspq_subcol.voyage
subset_lspq_subcol.loc[subset_lspq_subcol.voyage != 'AUCUN_VOYAGE','rta_exposure'] = subset_lspq_subcol.voyage

pd.set_option('display.max_columns', 20)
del subset_lspq_subcol['voyage']
#print(subset_lspq_subcol)

subset_gisaid_subcol = subset_gisaid.loc[:,('strain','virus','date','sex','age','country','division','country_exposure','division_exposure')]
subset_gisaid_subcol.insert(loc=7,column='rss',value='',allow_duplicates=True)
subset_gisaid_subcol.insert(loc=8,column='rta',value='',allow_duplicates=True)
subset_gisaid_subcol.insert(loc=11,column='rss_exposure',value='',allow_duplicates=True)
subset_gisaid_subcol.insert(loc=12,column='rta_exposure',value='',allow_duplicates=True)
subset_gisaid_subcol.loc[:,'rss'] = subset_gisaid_subcol.country
subset_gisaid_subcol.loc[:,'rta'] = subset_gisaid_subcol.country
subset_gisaid_subcol.loc[:,'rss_exposure'] = subset_gisaid_subcol.country_exposure
subset_gisaid_subcol.loc[:,'rta_exposure'] = subset_gisaid_subcol.country_exposure
#print(subset_gisaid_subcol)

#print(subset_lspq_subcol.columns)
#print(subset_gisaid_subcol.columns)

subset_lspq_subcol.to_csv(out_metadata,sep="\t",index=False)
subset_gisaid_subcol.to_csv(out_metadata,sep="\t",index=False,mode='a',header=False)
