import argparse
import sys

from scholar2scopus.scholar import scrape_author_publications_citations
from scholar2scopus.scopus import find_missing_citations_on_scopus


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--author', action="store", help='your name', required=True)
    parser.add_argument("--scopus_citations", action="store", default="scopus.csv",
                        help="csv file obtained from scopus with the list of papers that cite you",
                        )
    parser.add_argument('--scraper_api_key', action="store", help='API key for ScraperAPI', required=True)
    parser.add_argument('--report_path', action="store", help='path to the file where to write the report',
                        required=False, default='report.txt')
    parser.add_argument('--overwrite', action="store", help='overwrite files that were already downloaded',
                        required=False, default='False', choices=('True', 'False'))

    args = parser.parse_args()
    author = args.author
    scraper_api_key = args.scraper_api_key
    overwrite = args.overwrite == 'True'
    report_path = args.report_path
    scrape_author_publications_citations(author, overwrite, scraper_api_key)
    find_missing_citations_on_scopus(report_path=report_path)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
