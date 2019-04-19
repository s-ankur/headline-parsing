from wiktionaryparser import WiktionaryParser
parser = WiktionaryParser()

def capitalization(sent):
    ans = []
    for word in sent.split():
        if word.isupper():
            info = parser.fetch(word)
            print(info)
            if len(info[0]['definitions'])>0:
                ans.append(word)
            else:
                ans.append(word.lower())
        else:
            ans.append(word)
    return ' '.join(ans)




rules = [capitalization]


if __name__ =="__main__":
    ans=[]
    s=input()
    with open(s) as inp:
        for sent in inp.readlines():
            for rule in rules:
                sent= rule(sent)
            ans.append(sent)
    with open('canon_'+s,'w') as oup:
        oup.write('\n'.join(ans))
        
