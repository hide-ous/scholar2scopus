import argparse
import sys

from scholar2scopus.scholar import scrape_author_publications_citations


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--author', action="store", help='your name', required=True)
    parser.add_argument("--scopus_citations", action="store", default="scopus.csv",
                        help="csv file obtained from scopus with the list of papers that cite you",
                        )
    parser.add_argument('--scraper_api_key', action="store", help='api key for scraperapi', required=False, default=None)
    parser.add_argument('--overwrite', action="store", help='overwrite files that were already downloaded', required=False, default=False)

    args = parser.parse_args()
    author = args.author
    scraper_api_key = args.scraper_api_key
    overwrite = args.overwrite
    print('scraping', author)

    scrape_author_publications_citations(author, overwrite, scraper_api_key)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
