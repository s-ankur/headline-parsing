#!/usr/bin/env python
"""
Download News Headlines from popular Newspapers.
The output format is one headline per line which can be
stored in a file using the command
python download.py>headlines.txt
Note: Certain headlines may be malformed so as an error their urls are printed.
"""
import newspaper
import sys
from urllib.parse import urlsplit

indian_newspaper_urls = [r'https://www.cnbc.com/india/',
    r'https://zeenews.india.com/india',
    r'https://www.business-standard.com/',
    r'https://www.bloombergquint.com/',
    r'https://www.indiatoday.in/india',
    r'https://www.news18.com' ]

indian_newspaper_names = {urlsplit(url).hostname:url for url in indian_newspaper_urls}

if __name__ =="__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('newspaper',type=str,choices = indian_newspaper_names.keys(),
                        default = r'www.cnbc.com',metavar ='NEWSPAPER',
                        help='website of the newspaper from which to download the headlines from\n' +'\n'.join( indian_newspaper_names.keys()))
    args = parser.parse_args()

    try:
        paper_url = indian_newspaper_names[parser.newspaper]
        paper = newspaper.build(paper_url,memoize_articles=False)
        for article in paper.articles:
            article.download()
            if article and article.title and article.title.strip():
                print(article.title.strip())
            else:
                print(article.url,file=sys.stderr,)
    except KeyboardInterrupt:
        pass
