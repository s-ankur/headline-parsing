from stat_parser import Parser
parser = Parser()
f =open('tree.csv','w')
for i in open('5_Ankur.csv').readlines():
    f.write(' '.join(str(parser.parse(i)).split()))
    f.write('\n')
