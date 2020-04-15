"""
Eric Fournier 20200415
"""

import os
from SequenceSimulator import CreateFastaCovid
import random

location_file = os.path.join(os.path.dirname(os.getcwd()),"config/ordering.tsv")

class MetadataBuilder(object):
    def __init__(self, number_of_isolate, is_homogeneous, fasta_in, fasta_out):
        self.fasta_in = fasta_in
        self.fasta_out = fasta_out

        self.location_file = os.path.join(os.path.dirname(os.getcwd()),"config/ordering.tsv")
        self.number_of_isolate = number_of_isolate
        self.is_homogeneous = is_homogeneous

        self.header = {'Strain' : 'strain', 'Virus' : 'virus', 'Rta' : 'rta', 'CountryExposure' : 'coutry_exposure',
        'ProvinceExposure' : 'province_exposure', 'Rta_exposure' : 'rta_exposure', 'Segment' : 'segment', 'Length' : 'length',
        'Host' : 'host', 'Age' : 'age', 'Sex' : 'sex', 'LabOrig' : 'originating_lab', 'LabSubmt' : 'submitting_lab', 'Authors' : 'authors',
        'Url' : 'url', 'Title' : 'title'}


        self.location_dict = {'rta' : set(), 'province' : set(), 'country' : set()}
        self.rta_list = []
        self.province_list = []
        self.country_list = []


        self.random_rta_list = []
        self.random_province_list = []
        self.random_country_list = []

        #CreateFastaCovid(fasta_in_file = self.fasta_in, fasta_out_file = self.fasta_out, nb_seq = self.number_of_isolate, homogeneous = is_homogeneous)
        self.BuildLocationList()
#       self.CreateRandomRtaList()
        self.CreateRandomProvinceList()
        self.CreateRandomCountryList()

    def BuildLocationList(self): 
        with open(self.location_file) as readf:
            for line in readf:
                info = line.split('\t')
                self.location_dict[info[0]].add(info[1].strip('\n'))

        self.rta_list = list(self.location_dict['rta'] - self.location_dict['province'].union(self.location_dict['country']))
        self.province_list = list(self.location_dict['province'])
        self.country_list = list(self.location_dict['country'])

    def CreateRandomRtaList(self):
        for i in range(0,self.number_of_isolate):
            rnd_index = random.randint(0,len(self.rta_list - 1))
            self.random_rta_list.append(self.rta_list[rnd_index]) 

    def CreateRandomProvinceList(self):
        for i in range(0,self.number_of_isolate):
            rnd_index = random.randint(0,len(self.province_list) - 1)
            self.random_province_list.append(self.province_list[rnd_index]) 

    def CreateRandomCountryList(self):
        for i in range(0,self.number_of_isolate):
            rnd_index = random.randint(0,len(self.country_list) - 1)
            self.random_country_list.append(self.country_list[rnd_index]) 


fasta_in_file =  os.path.join(os.path.dirname(os.getcwd()),"data/gisaid_covid19_usa_1759.fasta")
fasta_in_file_test =  os.path.join(os.path.dirname(os.getcwd()),"data/three_seq.fasta")
fasta_out_10seq_homogeneous =  os.path.join(os.path.dirname(os.getcwd()),"data/covid19_10seq_homogeneous.fasta")
fasta_out_200seq_heterogeneous =  os.path.join(os.path.dirname(os.getcwd()),"data/covid19_200seq_heterogeneous.fasta")
fasta_out_10seq_heterogeneous =  os.path.join(os.path.dirname(os.getcwd()),"data/covid19_10seq_heterogeneous.fasta")
number_of_isolate = 10
is_homogeneous_seq = False

mbuilder = MetadataBuilder(number_of_isolate, is_homogeneous_seq, fasta_in_file, fasta_out_10seq_homogeneous)
#print(mbuilder.random_rta_list)
#print(mbuilder.random_province_list)
print(mbuilder.random_country_list)
