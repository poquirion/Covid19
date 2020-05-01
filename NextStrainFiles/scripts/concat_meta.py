#!/usr/bin/env python3
import argparse
import datetime
import glob
import os
import random

import pandas as pd
import unidecode
from country_list import countries_for_language


def count_fasta_len(fastas):
    id_len = {}
    for fasta in fastas:
        with open(fasta) as fp:
            fasta_id = fp.readline().lstrip('>').split('/')[0]
            id_len[fasta_id] = len(fp.read())

    return id_len


def main():
    parser = argparse.ArgumentParser(
        description="concat_meta_tsv",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("--inspq_meta", default='data/sgil_extract.tsv', help="The LNSPQ .tsv")
    parser.add_argument("--nextstrain_metadata", help="The .tsv that comes by "
                                                                                       "with nextstrain")
    parser.add_argument("--fasta_dir", default=None, help="The modified .tsv")
    parser.add_argument("--output", default='data/merged_metadata.tsv', help="The modified .tsv")
    parser.add_argument("--subsample", '-s', type=int,
                        default=None, help="A metadata file with N sample and all QC ones")


    args = parser.parse_args()
    in_path = args.nextstrain_metadata
    out_path = args.output
    subsample = args.subsample
    lnspq_path = args.inspq_meta
    fasta_dir = args.fasta_dir
    # exluded = args.nextstrain_exclude

    gsaid_df = pd.read_csv(in_path, sep='\t')
    lnspq_df = pd.read_csv(lnspq_path, sep='\t')

    # traduction from fr to en
    traduc = {'NO_LSPQ': 'strain',
              'AGE': 'age',
              'SEX': 'sex',
              'RSS_PATIENT': 'rss',
              'VOYAGE_PAYS_1': 'country_exposure',
              'DATE_PRELEV': 'date',
              'DATE_RECU': 'date_submitted',
              'CH': 'originating_lab',
              'POSTAL_CODE': 'rta'}
    lnspq_df.rename(columns=traduc, inplace=True)

    lnspq_df['country_exposure'] = [unidecode.unidecode(p.title()) for p in lnspq_df['country_exposure']]
    # lnspq_df['date_submitted'] = "{}s".format(datetime.datetime.today())
    pays_qc = {k: unidecode.unidecode(v) for k, v in countries_for_language('fr_CA')}

    pays_anglo = dict(countries_for_language('en'))
    # Fix non stadard names
    pays_anglo['US'] ='USA'
    pays_anglo['HK'] = 'Hong Kong'
    pays_anglo['CZ'] = 'Czech Republic'
    pays_anglo['CD'] = 'Democratic Republic of the Congo'

    trans = {pays_qc[code]: pays_anglo[code] for code in pays_qc.keys()}
    trans['Aucun_Voyage'] = '?'
    lnspq_df['country_exposure'].replace(trans, inplace=True)
    lnspq_df['rta_exposure'] = lnspq_df['country_exposure']

    fastas = glob.glob("{}/*fasta".format(fasta_dir))
    fasta_id_len = count_fasta_len(fastas)

    for fid, l in fasta_id_len.items():
        lnspq_df.loc[lnspq_df['strain'] == fid, 'lenth'] = l

    lnspq_df['virus'] = 'ncov'
    lnspq_df['title'] = 'CoVSeQ - Covid Sequencing Quebec'
    lnspq_df['country'] = 'Quebec'
    lnspq_df['location'] = 'Quebec'
    lnspq_df['division'] = 'Quebec'
    lnspq_df['region'] = 'North America'
    lnspq_df['submitting_lab'] = 'LSPQ'


    if fasta_dir:
        lnspq_df['url'] = 'http://www.covseq.ca/data/{}'.format(os.path.basename(fasta_dir.strip('/')))
    else:
        lnspq_df['url'] = ''

    # add rta and rss entry to world

    # still need to fix Iles 'Turques-Caiques' and 'Iles Vierges (E-U)',

    neighbourg = ['New York', 'Ontario', 'Vermont', 'New Hampshire',
                  "Massachusetts", 'Maine', 'New Brunswick', 'Grand Princess']

    gsaid_df.loc[gsaid_df['region'] != 'North America', 'rss'] = gsaid_df['country']
    gsaid_df.loc[gsaid_df['region'] != 'North America', 'rta'] = gsaid_df['country']
    gsaid_df.loc[gsaid_df['region'] == 'North America', 'rss'] = gsaid_df['country']


    gsaid_df.loc[gsaid_df['region'] == 'North America', 'rta'] = gsaid_df['country']
    gsaid_df.loc[gsaid_df['division'].isin(neighbourg), 'rss'] = gsaid_df['division']

    gsaid_df['rta_exposure'] = gsaid_df['country_exposure']


    # neighbourg

    # rta_country

    # table.assign(region=)
    pd.concat([lnspq_df, gsaid_df], sort=False).to_csv(out_path, sep='\t', index=False)

    if subsample:
        name = os.path.basename(out_path)
        path = os.path.dirname(out_path)
        s_path = '{}/sampled_{}'.format(path, name)
        print('subsample with {} point in {}'.format(subsample, s_path))
        s_df = gsaid_df.iloc[random.sample(range(len(gsaid_df)), subsample)]

        # make sure root virus is in data
        extra = []
        for s in open('../config/include.txt').read().splitlines():
            if s not in s_df['strain']:
                extra = extra + [gsaid_df.loc[gsaid_df['strain'] == s]]

        pd.concat([lnspq_df, s_df] + extra).to_csv(s_path, sep='\t', index=False)



if __name__ == '__main__':
    main()
