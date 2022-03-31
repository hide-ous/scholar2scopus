import json
import pickle
from collections import defaultdict
from functools import partial

import pandas as pd
from scholarly import scholarly
from thefuzz import process

SCOPUS_CITATIONS = 'scopus.csv'


def find_missing_citations_on_scopus(report_path='report.txt', min_fuzzy_match_score=90):
    scopus_df = pd.read_csv(SCOPUS_CITATIONS)

    scopus_titles = scopus_df.Title.tolist()

    def extract_field(bib, field):
        if field in bib:
            return bib[field]
        else:
            return None

    def print_bib(bib):
        return json.dumps(dict(filter(lambda x: x[0] != 'abstract', bib.items())), indent=4)

    scholar_df = pd.read_json('publications.json', orient='index')
    scholar_df['year'] = scholar_df.bib.apply(partial(extract_field, field='pub_year'))
    scholar_df['title'] = scholar_df.bib.apply(partial(extract_field, field='title'))
    scholar_df['journal'] = scholar_df.bib.apply(partial(extract_field, field='journal'))

    with open('scholar_citations.pkl', 'rb') as f:
        scholar_citations = pickle.load(f)

    missing_citations = defaultdict(list)
    for pubidx, scholar_citations in scholar_citations.items():

        for scholar_citation in scholar_citations:
            scholar_title = scholar_citation['bib']['title']
            best_scopus_title, best_scopus_title_score = process.extractOne(scholar_title, scopus_titles)
            if best_scopus_title_score > min_fuzzy_match_score:  # arbitrary threshold for fuzzy match similarity
                continue
            else:
                missing_citations[pubidx].append(scholar_citation)

    def filter_citation(citation):
        bib = defaultdict(lambda: "", citation['bib'])
        if bib["pub_type"] in ["phdthesis"]:
            return False
        if ('arXiv' in bib['venue']) or ('arXiv' in bib['journal']):
            return False
        return True

    strings = list()
    for pubidx, scholar_citations in missing_citations.items():
        strings.append("The publication:")
        strings.append(print_bib(scholar_df.loc[pubidx].bib))
        strings.append('is missing the following citations:')
        for scholar_citation in filter(filter_citation, scholar_citations):
            try:
                the_string = scholarly.bibtex(scholar_citation['bib'])
            except KeyError:
                the_string = print_bib(scholar_citation['bib'])
            strings.append(the_string)
        strings.append('\n********************************************\n')
    with open(report_path, 'w+') as f:
        f.write('\n'.join(strings))


if __name__ == '__main__':
    find_missing_citations_on_scopus()
