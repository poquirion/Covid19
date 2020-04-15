"""
Eric Fournier 20200415
"""

import os
from SequenceSimulator import CreateFastaCovid
import random
import datetime


location_file = os.path.join(os.path.dirname(os.getcwd()),"config/ordering.tsv")

class RandomDataGenerator(object):
    def __init__(self):
        pass

    def CreateRandomList(self, target_length, data_list):
        rnd_list = [] 

        for i in range(0,target_length):
            rnd_index = random.randint(0,len(data_list) - 1)
            rnd_list.append(data_list[rnd_index]) 

        return(rnd_list.copy())

    def CreateRandomDateList(self,target_length):
        start_date = datetime.date(year=2018, month=1, day=1)
        end_date = datetime.date(year=2020, month=11, day=1)
        rnd_date_list = []

        for j in range(0, target_length):
            time_between_dates = end_date - start_date
            days_between_dates = time_between_dates.days
            random_number_of_days = random.randrange(days_between_dates)
            random_date = start_date + datetime.timedelta(days=random_number_of_days)
            rnd_date_list.append(str(random_date))

        return(rnd_date_list.copy())

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

        self.rnd_generator = RandomDataGenerator()

        self.random_rta_list = None
        self.random_province_list = None
        self.random_country_list = None
        self.random_date_list = None

        #CreateFastaCovid(fasta_in_file = self.fasta_in, fasta_out_file = self.fasta_out, nb_seq = self.number_of_isolate, homogeneous = is_homogeneous)
        self.BuildLocationList()
        self.CreateRandomData()

    def CreateRandomData(self):
        self.random_rta_list = self.rnd_generator.CreateRandomList(self.number_of_isolate,self.rta_list)
        self.random_province_list = self.rnd_generator.CreateRandomList(self.number_of_isolate,self.province_list)
        self.random_country_list = self.rnd_generator.CreateRandomList(self.number_of_isolate,self.country_list)
        self.random_date_list = self.rnd_generator.CreateRandomDateList(self.number_of_isolate)

    def BuildLocationList(self): 
        with open(self.location_file) as readf:
            for line in readf:
                info = line.split('\t')
                self.location_dict[info[0]].add(info[1].strip('\n'))

        self.rta_list = list(self.location_dict['rta'] - self.location_dict['province'].union(self.location_dict['country']))
        self.province_list = list(self.location_dict['province'])
        self.country_list = list(self.location_dict['country'])

'''
    def CreateRandomDateList(self):
        for j in range(1, 10):
            time_between_dates = end_date - start_date
            days_between_dates = time_between_dates.days
            random_number_of_days = random.randrange(days_between_dates)
            random_date = start_date + datetime.timedelta(days=random_number_of_days)
            # print(random_date)
'''


fasta_in_file =  os.path.join(os.path.dirname(os.getcwd()),"data/gisaid_covid19_usa_1759.fasta")
fasta_in_file_test =  os.path.join(os.path.dirname(os.getcwd()),"data/three_seq.fasta")
fasta_out_10seq_homogeneous =  os.path.join(os.path.dirname(os.getcwd()),"data/covid19_10seq_homogeneous.fasta")
fasta_out_200seq_heterogeneous =  os.path.join(os.path.dirname(os.getcwd()),"data/covid19_200seq_heterogeneous.fasta")
fasta_out_10seq_heterogeneous =  os.path.join(os.path.dirname(os.getcwd()),"data/covid19_10seq_heterogeneous.fasta")
number_of_isolate = 10
is_homogeneous_seq = False

mbuilder = MetadataBuilder(number_of_isolate, is_homogeneous_seq, fasta_in_file, fasta_out_10seq_homogeneous)
print(mbuilder.random_rta_list)
print(mbuilder.random_province_list)
print(mbuilder.random_country_list)
print(mbuilder.random_date_list)
