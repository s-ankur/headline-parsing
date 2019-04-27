#!/usr/bin/env python
"""
Parse the given sentence using a parser such as Stanford Parser, PyStatParser or AllenNlp Parser
Takes input in the form of a file of newline seperated sentences and outputs the parse in a similar format.
The parse notation of various parsers may be significantly different.
"""

import nltk.tree


class stanford:
    def parse(self, line):
        from urllib.parse import urlencode, quote_plus
        import bs4
        import requests
        q = urlencode({'query': line}, quote_via=quote_plus)
        URL = "http://nlp.stanford.edu:8080/parser?" + q
        r = requests.get(URL)
        soup = bs4.BeautifulSoup(r.content, 'html5lib')
        return ' '.join(soup.find('pre').text.split())


class pystat:
    def __init__(self):
        from stat_parser import Parser
        self.parser = Parser()

    def parse(self, line):
        return ' '.join(str(self.parser.parse(line)).split())


class allen:
    def __init__(self):
        from allennlp.models.archival import load_archive
        from allennlp.service.predictors import Predictor
        archive = load_archive(
            "https://s3-us-west-2.amazonaws.com/allennlp/models/elmo-constituency-parser-2018.03.14.tar.gz"
        )
        self.predictor = Predictor.from_archive(archive, 'constituency-parser')

    def parse_allen(self, line):
        return ' '.join(self.predictor.predict_json({"sentence": line}).split())


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=str,
                        help='input file')
    parser.add_argument('-p', '--parser', type=str, choices=['pystat', 'stanford', 'allen'],
                        default='stanford',
                        help='parser to be used')
    args = parser.parse_args()
    sent_parser = vars()[args.parser]()
    with open(args.file) as infile, open(args.file[:-4] + '_parsed_' + args.parser + args.file[-4:], 'w') as outfile:
        for line in infile.readlines():
            parsed = sent_parser.parse(line)
            outfile.write(parsed)
            outfile.write('\n')
