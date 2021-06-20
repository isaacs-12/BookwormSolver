# Calls LetterGetter to get a graph of letters that can be traversed to generate words to try in Clicker

from typing import Mapping
import LetterGetter

dictFile = "TestWords.txt"
allWords = "FullUncompressedDict.txt"

foundWords = []

# types
Graph = Mapping[int, LetterGetter.Node]

# helpers
def genWordFromPath(graph: Graph, path):
    word = ""
    for id in path:
        word += str(graph[id].value)
    return word

def find_all_words(graph: Graph, startNode: LetterGetter.Node, prefixes, validWords, path):
    global foundWords

    soFar = genWordFromPath(graph, path)

    if soFar in validWords and len(soFar) >= 3:
        # We found a valid word but aren't necessarily at a dead end
        foundWords += [soFar]
    for n in graph[startNode.nodeId].edges:
        newNode = graph[n]
        if newNode.nodeId not in path:
            newPath = path + [newNode.nodeId]
            if str(genWordFromPath(graph, newPath)) not in prefixes:
                # We are at a dead end/went too far
                continue
            return find_all_words(graph, newNode, prefixes, validWords, newPath)

def traverseGraph(graph: Graph, prefixes, validWords):
    for start in graph.keys():
        startNode = graph[start]
        if str(startNode.value) not in prefixes:
            continue
        find_all_words(graph, startNode, prefixes, validWords, [startNode.nodeId])
    return


def getPrefixes(validWords):
    prefixes = []
    for w in validWords:
        soFar = ''
        for c in w:
            soFar += c
            prefixes.append(str(soFar))
    return set(prefixes)

def dictWords(words):
    newWords = []
    for word in words:
        newWords.append(word.split('\n')[0])
    wordSet = set(newWords)
    return wordSet

def main():
    graph = LetterGetter.main()
    words = open(allWords, 'r').readlines()

    validWords = dictWords(words)
    print(len(validWords))

    prefixes = getPrefixes(validWords)
    print(len(prefixes))
    
    traverseGraph(graph, prefixes, validWords)
    global foundWords
    print("Found words: {}".format(foundWords))

main()