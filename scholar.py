import json

from scholarly import scholarly
from tqdm import tqdm


def get_author(name):
    search_query = scholarly.search_author(name)
    first_author_result = next(search_query)
    author = scholarly.fill(first_author_result)
    return author


def get_publications(author):
    return list(map(scholarly.fill, author['publications']))


# def get_citations(publication):
#     return list(map(scholarly.fill, scholarly.citedby(publication)))

def get_citations(publication):
    return list(map(scholarly.fill, tqdm(scholarly.citedby(publication),
                                         'citations for {}'.format(publication['bib']['title']),
                                         publication['num_citations']
                                         )))


def scrape_author_publications_citations(name):
    author = get_author(name)

    with open('author.json', 'w+', encoding='utf8') as f:
        json.dump({k: v for k, v in author.items() if k != 'source'}, f)

    publications = dict(enumerate(get_publications(author)))
    with open('publications.json', 'w+', encoding='utf8') as f:
        json.dump({k: v for k, v in publications.items() if k != 'source'}, f)

    citations = dict()
    for idx, publication in publications.items():
        current_citations = get_citations(publication)
        citations[idx] = current_citations
    with open('citations.json', 'w+', encoding='utf8') as f:
        json.dump({k: v for k, v in citations.items() if k != 'source'}, f)


if __name__ == '__main__':
    scrape_author_publications_citations('Your Name')
