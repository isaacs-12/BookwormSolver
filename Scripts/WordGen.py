# Calls LetterGetter to get a graph of letters that can be traversed to generate words to try in Clicker

from typing import Mapping
import LetterGetter
import time

dictFile = "../Dicts/TestWords.txt"
allWords = "../Dicts/FullUncompressedDict.txt"

foundWords = []
prefixes = set([])
validWords = set([])
checkedWords = 0

# types
Graph = Mapping[int, LetterGetter.Node]

# helpers
def genWordFromPath(graph: Graph, path):
    word = ""
    for id in path:
        word += str(graph[id].value)
    return word

def FindAllWords(graph: Graph, startNode: LetterGetter.Node, path):
    global foundWords
    global checkedWords
    checkedWords += 1
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
            FindAllWords(graph, newNode, newPath)

def traverseGraph(graph: Graph):
    for start in graph.keys():
        startNode = graph[start]
        if str(startNode.value) not in prefixes:
            continue
        FindAllWords(graph, startNode, [startNode.nodeId])
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
    newWords = set([])
    for word in words:
        newWords.add(word.split('\n')[0])
    return newWords

def main():
    graph = LetterGetter.main()
    words = open(allWords, 'r').readlines()

    global validWords
    validWords = dictWords(words)
    print(len(validWords))

    global prefixes
    prefixes = getPrefixes(validWords)
    print(len(prefixes))
    
    start_time = time.time()
    traverseGraph(graph)
    cur_time = time.time()
    print("Traversal took {} seconds.".format((cur_time-start_time)))
    global foundWords
    global checkedWords
    # print("Checked words: {}".format(checkedWords))
    print("Found words: {}".format(len(foundWords)))

main()