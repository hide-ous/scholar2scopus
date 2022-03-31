import json
import pickle
from collections import defaultdict
from functools import partial

import pandas as pd
from scholarly import scholarly
from thefuzz import process

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
            if best_scopus_title_score > 90:
                print('match', best_scopus_title_score, scholar_title, '\n', best_scopus_title)
                continue
            else:
                print('no match', best_scopus_title_score, scholar_title, '\n', best_scopus_title)
                missing_citations[pubidx].append(scholar_citation)

            # citation_authors = scholar_citation['bib']['author']
            #
            #
            # hasmatch = False
            # for scopus_idx, scopus_row in scopus_df.iterrows():
            #     scopus_title = scopus_row.Title
            #
            #
            #
            #     scopus_authors = scopus_row.last_names
            #     sameauthors = True
            #     if len(scopus_authors) != len(citation_authors):
            #         sameauthors = False
            #     else:
            #         for name1, name2 in zip(scopus_authors, citation_authors):
            #             if not name2.lower().endswith(name1.lower()):
            #                 sameauthors = False
            #                 break
            #     if sameauthors:
            #         print('found match', scopus_authors, citation_authors)
            #         hasmatch = True
            #         break
            # if not hasmatch:
            #     print('no match for ', scholar_citation['bib']['title'])

    def filter_citation(citation):
        bib = defaultdict(lambda:"", citation['bib'])
        if bib["pub_type"] in ["phdthesis"]:
            return False
        if ('arXiv' in bib['venue']) or ('arXiv' in bib['journal']):
            return False
        return True

    strings = list()
    for pubidx, scholar_citations in missing_citations.items():
        print(pubidx)
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
    print('\n'.join(strings))
