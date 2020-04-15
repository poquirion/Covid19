"""
Eric Fournier 20200415
"""

import os
from SequenceSimulator import CreateFastaCovid

fasta_in_file =  os.path.join(os.path.dirname(os.getcwd()),"data/gisaid_covid19_usa_1759.fasta")
fasta_in_file_test =  os.path.join(os.path.dirname(os.getcwd()),"data/three_seq.fasta")
fasta_out_10seq_homogeneous =  os.path.join(os.path.dirname(os.getcwd()),"data/covid19_10seq_homogeneous.fasta")
fasta_out_200seq_heterogeneous =  os.path.join(os.path.dirname(os.getcwd()),"data/covid19_200seq_heterogeneous.fasta")
fasta_out_10seq_heterogeneous =  os.path.join(os.path.dirname(os.getcwd()),"data/covid19_10seq_heterogeneous.fasta")

location_file = os.path.join(os.path.dirname(os.getcwd()),"config/ordering.tsv")

#CreateFastaCoivid(fasta_in_file = fasta_in_file, fasta_out_file=fasta_out_10seq_heterogeneous, nb_seq=10, homogeneous=False)


class MetadataBuilder(object):
    def __init__(self):

        self.header = {'Strain' : 'strain', 'Virus' : 'virus', 'Rta' : 'rta', 'CountryExposure' : 'coutry_exposure',
        'ProvinceExposure' : 'province_exposure', 'Rta_exposure' : 'rta_exposure', 'Segment' : 'segment', 'Length' : 'length',
        'Host' : 'host', 'Age' : 'age', 'Sex' : 'sex', 'LabOrig' : 'originating_lab', 'LabSubmt' : 'submitting_lab', 'Authors' : 'authors',
        'Url' : 'url', 'Title' : 'title'}


        self.location_dict = {'rta' : set(), 'province' : set(), 'country' : set()}
        self.rta_list = []
        self.province_list = []
        self.country_list = []

    def BuildLocationList(self): 
        with open(location_file) as readf:
            for line in readf:
                info = line.split('\t')
                self.location_dict[info[0]].add(info[1].strip('\n'))

        self.rta_list = list(self.location_dict['rta'] - self.location_dict['province'].union(self.location_dict['country']))
        self.province_list = list(self.location_dict['province'])
        self.country_list = list(self.location_dict['country'])

mbuilder = MetadataBuilder()
mbuilder.BuildLocationList()

