import argparse

from scholar import scrape_author_publications_citations

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--author', action="store", help='your name', required=True)
    parser.add_argument("--scopus_citations", action="store", default="scopus.csv",
                        help="csv file obtained from scopus with the list of papers that cite you",
                        )

    args = parser.parse_args()
    author = args.author
    print('scraping', author)

    scrape_author_publications_citations(author)
