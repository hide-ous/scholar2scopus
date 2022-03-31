import json
import os.path
import pickle
from time import sleep
from random import randint

# from fp.fp import FreeProxy
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

    for citation in map(scholarly.fill, tqdm(scholarly.citedby(publication),
                                             'citations for {}'.format(publication['bib']['title']),
                                             publication['num_citations']
                                             )):
        citations.append(citation)
        sleep_time = randint(1, 60)
        # print("sleeping {} seconds".format(sleep_time))
        sleep(sleep_time)

    return citations


def refresh_proxy(scraper_api_key = None):
    pg = ProxyGenerator()

    # proxy = FreeProxy(rand=True, timeout=1, country_id=['IT']).get()
    # pg.SingleProxy(http=proxy, https=proxy)
    # pg.FreeProxies()
    success = pg.ScraperAPI(scraper_api_key)
    print(success and "connected to proxy" or "could not connect to proxy")
    scholarly.use_proxy(pg)


def scrape_author_publications_citations(name, force_download=False, scraper_api_key = None):
    refresh_proxy(scraper_api_key)

    if os.path.exists('author.pkl') and not force_download:
        with open('author.pkl', 'rb') as f:
            author = pickle.load(f)
    else:
        author = get_author(name)
        with open('author.json', 'w+', encoding='utf8') as f:
            json.dump({k: v for k, v in author.items() if k != 'source'}, f)
        with open('author.pkl', 'wb+') as f:
            pickle.dump(author, f)

    if os.path.exists('publications.pkl') and not force_download:
        with open('publications.pkl', 'rb') as f:
            publications = pickle.load(f)
    else:
        publications = dict(enumerate(get_publications(author)))
        with open('publications.json', 'w+', encoding='utf8') as f:
            json.dump({k: v for k, v in publications.items() if k != 'source'}, f)
        with open('publications.pkl', 'wb+') as f:
            pickle.dump(publications, f)

    if os.path.exists('scholar_citations.pkl') and not force_download:
        pass
    else:
        citations = dict()
        for idx, publication in publications.items():
            done = False
            if publication['num_citations'] == 0:
                done = True
            while not done:
                try:
                    current_citations = get_citations(publication)
                    citations[idx] = current_citations
                    done = True
                except Exception as e:
                    print(e)
                    print(publication)
                    sleep_time = randint(1, 180)
                    print('sleeping for {} seconds before retrying'.format(sleep_time))
                    sleep(sleep_time)
                    refresh_proxy(scraper_api_key)

        with open('scholar_citations.json', 'w+', encoding='utf8') as f:
            json.dump({k: v for k, v in citations.items() if k != 'source'}, f)
        with open('scholar_citations.pkl', 'wb+') as f:
            pickle.dump(citations, f)


if __name__ == '__main__':
    scrape_author_publications_citations('Your Name')
