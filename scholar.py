import json
import os.path
import pickle

from fp.fp import FreeProxy
from tqdm import tqdm

from scholarly import scholarly, ProxyGenerator


def get_author(name):
    search_query = scholarly.search_author(name)
    first_author_result = next(search_query)
    author = scholarly.fill(first_author_result)
    return author


def get_publications(author):
    return list(map(scholarly.fill,
                    tqdm(author['publications'],
                         'collecting publications'
                         )
                    ))


# def get_citations(publication):
#     return list(map(scholarly.fill, scholarly.citedby(publication)))

def get_citations(publication):
    citations = list()
    for citation in tqdm(scholarly.citedby(publication),
                         'citations for {}'.format(publication['bib']['title']),
                         publication['num_citations']
                         ):
        citations.append(citation)

    return citations


def scrape_author_publications_citations(name):
    pg = ProxyGenerator()

    proxy = FreeProxy(rand=True, timeout=1, country_id=['IT']).get()
    pg.FreeProxies()
    # pg.SingleProxy(http=proxy, https=proxy)
    scholarly.use_proxy(pg)

    if os.path.exists('author.pkl'):
        with open('author.pkl', 'rb') as f:
            author = pickle.load(f)
    else:
        author = get_author(name)
        with open('author.json', 'w+', encoding='utf8') as f:
            json.dump({k: v for k, v in author.items() if k != 'source'}, f)
        with open('author.pkl', 'wb+') as f:
            pickle.dump(author, f)

    if os.path.exists('publications.pkl'):
        with open('publications.pkl', 'rb') as f:
            publications = pickle.load(f)
    else:
        publications = dict(enumerate(get_publications(author)))
        with open('publications.json', 'w+', encoding='utf8') as f:
            json.dump({k: v for k, v in publications.items() if k != 'source'}, f)
        with open('publications.pkl', 'wb+') as f:
            pickle.dump(publications, f)

    if os.path.exists('citations.pkl'):
        with open('citations.pkl', 'rb') as f:
            citations = pickle.load(f)
    else:
        citations = dict()
        for idx, publication in publications.items():
            try:
                current_citations = get_citations(publication)
                citations[idx] = current_citations
            except Exception as e:
                print(e)
                print(publication)
        with open('citations.json', 'w+', encoding='utf8') as f:
            json.dump({k: v for k, v in citations.items() if k != 'source'}, f)
        with open('citations.pkl', 'wb+') as f:
            pickle.dump(citations, f)


if __name__ == '__main__':
    scrape_author_publications_citations('Your Name')
