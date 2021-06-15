# Calls LetterGetter to get a graph of letters that can be traversed to generate words to try in Clicker

import LetterGetter

dictFile = r"C:\Users\Isaac\Documents\BookwormSolver\TestWords.txt"

def genWordFromPath(graph, ids):
    word = ''
    for id in ids:
        word += graph[id].value

def find_all_words(graph, start, end, prefixes, path=[]):
    paths = []
    newPath = path + [start]
    soFar = genWordFromPath(graph, newPath)
    if soFar not in prefixes:
        print(soFar)
        return soFar
    if start == end:
        return soFar
    if not start in graph.keys():
        return
    for node in graph[start].edges:
        if node not in path:
            newPaths = find_all_words(graph, node, end, prefixes, newPath)
            for p in newPaths:
                paths.append(p)
    return paths

def traverseGraph(graph, prefixes):
    foundWords = []
    for start in graph.keys():
        for end in graph.keys():
            if start == end:
                continue
            words = find_all_words(graph, start, end, [], prefixes)
            foundWords += words
    return foundWords


def getPrefixes(validWords):
    prefixes = []
    for w in validWords:
        soFar = ''
        for c in w.split():
            soFar += c
            prefixes.append(soFar)
    return set(prefixes)

def dictWords(words):
    newWords = []
    for word in words:
        newWords.append(word.split('\n')[0])
    wordSet = set(newWords)
    return wordSet

def main():
    graph = LetterGetter.main()
    words = open(dictFile, 'r').readlines()

    validWords = dictWords(words)
    print("ValidWords List: {}\n".format(validWords))

    prefixes = getPrefixes(validWords)
    print("Prefixes List: {}\n".format(prefixes))
    
    foundWords = traverseGraph(graph, prefixes)
    print("Found words: {}".format(foundWords))

main()