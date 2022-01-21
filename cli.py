import json

from scholarly import scholarly

if __name__ == '__main__':

    # Retrieve the author's data, fill-in, and print
    # Get an iterator for the author results
    search_query = scholarly.search_author('Your Name')
    # Retrieve the first result from the iterator
    first_author_result = next(search_query)
    scholarly.pprint(first_author_result)

    # Retrieve all the details for the author
    author = scholarly.fill(first_author_result)
    scholarly.pprint(author)
    with open('author.json', 'w+', encoding='utf8') as f:
        json.dump({k: v for k, v in author.items() if k != 'source'}, f)

    publications = dict(enumerate(map(scholarly.fill, author['publications'])))
    with open('publications.json', 'w+', encoding='utf8') as f:
        json.dump({k: v for k, v in publications.items() if k != 'source'}, f)

    citations = dict()
    for idx, publication in publications.items():
        scholarly.pprint(publication)

        # Which papers cited that publication?
        current_citations = list(map(scholarly.fill, scholarly.citedby(publication)))
        print(current_citations)
        citations[idx] = current_citations
    with open('citations.json', 'w+', encoding='utf8') as f:
        json.dump({k: v for k, v in citations.items() if k != 'source'}, f)
