import re

compressedPath = 'FullCompressedDict.txt'
uncompressedPath = 'FullUncompressedDict.txt'

compressedWords = []
uncompressedWords = []

words = open(compressedPath, 'r').readlines()
for word in words:
    compressedWords.append(word.split('\n')[0])

prev = compressedWords[0]
for c in compressedWords:
    lint = re.findall(r'\d+', c)
    stri = re.findall(r'[a-zA-Z]+', c)
    prefix = ''
    if len(lint) != 0:
        prefix = prev[:int(lint[0])]
    else:
        prefix = prev
    next = prefix + stri[0]
    uncompressedWords.append(next)
    prev = next

with open(uncompressedPath, 'w') as f:
    for w in uncompressedWords:
        f.write("%s\n" % w)