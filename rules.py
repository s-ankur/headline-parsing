#!/usr/bin/env python
"""
Apply all the rules to a file in the same format as generted by headlines.py.
Currently Implemented Rule: Capitalization(C) Quote(Q) Is(I)
"""
from collections import OrderedDict
from wiktionaryparser import WiktionaryParser
import parse
import nltk


class capitalization:
    def __init__(self):
        self.parser = WiktionaryParser()

    def apply(self, sent):
        ans = []
        for word in sent.split():
            if word.isupper():
                info = self.parser.fetch(word)
                if len(info[0]['definitions']) > 0:
                    ans.append(word)
                else:
                    ans.append(word.lower())
            else:
                ans.append(word)
        return ' '.join(ans)

class verb_add:
    def __init__(self):
        self.stanford = parse.stanford()
        self.pystat =parse.pystat()

    def mismatch(self,sent):
        parse1=self.pos(sent,self.stanford)
        parse2=self.pos(sent,self.pystat)
        for token1, token2 in zip(parse1,parse2):

            if token1[1].startswith('N') and token2[1].startswith('V'):
                return token1[0]
            
    def pos(self,sent,parser):
        return nltk.Tree.fromstring(parser.parse(sent)).pos()

    def apply(self,sent):
        mismatch= self.mismatch(sent)
        if mismatch:
            return sent.replace(mismatch,'is '+mismatch)
        return sent

class strip_quotes:
    quotes = "'`"+'"'+"‘’"
    def apply(self,sent):
        return ''.join([i for i in sent if i not in self.quotes])

rules = OrderedDict((
        ('Q',strip_quotes()),
        ('C',capitalization()),
        ('I',verb_add()),
))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=str,
                        help='input file')
    parser.add_argument('-e','--exclude',type = str,default='',
                        help = f'rule to exclude {list(rules.keys())}')
    args = parser.parse_args()
    ans = []
    with open(args.file) as infile:
        for sent in infile.readlines():
            sent= sent.strip()
            for rule in rules:
                if rule not in args.exclude:
                    sent = rules[rule].apply(sent)
            ans.append(sent)
    with open(args.file[:-4] + '_canonical_gen' + args.file[-4:], 'w') as outfile:
        outfile.write('\n'.join(ans))
