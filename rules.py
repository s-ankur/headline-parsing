#!/usr/bin/env python
"""
Apply all the rules to a file in the same format as generted by headlines.py.
Currently Implemented Rule: Capitalization
"""

from wiktionaryparser import WiktionaryParser
from stat_parser import Parser


class capitalization:
    def __init__(self):
        self.parser = WiktionaryParser()

    def apply(self, sent):
        ans = []
        for word in sent.split():
            if word.isupper():
                info = self.parser.fetch(word)
                print(info)
                if len(info[0]['definitions']) > 0:
                    ans.append(word)
                else:
                    ans.append(word.lower())
            else:
                ans.append(word)
        return ' '.join(ans)


rules = {
    "CAP": capitalization(),
}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=str,
                        help='input file')
    args = parser.parse_args()
    sent_parser = vars()[args.parser]()

    ans = []
    with open(args.file) as infile:
        for sent in infile.readlines():
            for rule in rules.values():
                sent = rule(sent)
            ans.append(sent)
    with open(args.file[:-4] + '_canonical_gen' + args.file[-4:], 'w') as outfile:
        outfile.write('\n'.join(ans))
