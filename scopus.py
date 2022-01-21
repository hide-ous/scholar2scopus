import json
from functools import partial

import pandas as pd

SCOPUS_CITATIONS = 'scopus.csv'

if __name__ == '__main__':
    scopus_df = pd.read_csv(SCOPUS_CITATIONS)


    def scopus_last_names(author_string):
        # for each author in scopus, take just the last name
        # break down the authors in scholar
        # each last name from scopus should match one (the last?) token in scholar
        # corner cases: individuals changing names, multiple last names
        return list(map(lambda x: x[:x.index(',')], author_string.split('.,')))


    scopus_df['last_names'] = scopus_df.Authors.apply(scopus_last_names)

    scholar_df = pd.read_json('publications.json', orient='index')


    def extract_field(bib, field):
        if field in bib:
            return bib[field]
        else:
            return None


    scholar_df['year'] = scholar_df.bib.apply(partial(extract_field, field='pub_year'))
    scholar_df['title'] = scholar_df.bib.apply(partial(extract_field, field='title'))
    scholar_df['journal'] = scholar_df.bib.apply(partial(extract_field, field='journal'))

    # for entry in