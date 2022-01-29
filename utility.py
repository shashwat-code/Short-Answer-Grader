"""
finding neighbours, parents child there relation with eachother which will be used in alignment of sentences
"""
from config import *
from nltk_utility import *


class utlity:

    '''
    checking for sublist
    Input: list A & B
    Output: True or false i.e whether B is sublist of A or not
    '''

    @staticmethod
    def is_sublist(A, B):

        flag = True
        for item in A:
            if item not in B:
                flag = False
                break
        return flag

    '''
    common neighbours of words
    Input: list of words
    Output: list of common neighbour words
    '''

    def get_commonNeighboringWords(self, sourceWords, targetWords, convertToLowerCase=True):

        commonNeighboringWords = []
        a = []
        b = []
        if convertToLowerCase:
            for i in sourceWords:
                a.append(i.lower())
            for j in targetWords:
                b.append(j.lower())

        swapped = False
        if len(a) > len(b):
            temp = a
            a = b
            b = temp
            swapped = True

        maximumSize = len(a)
        for size in range(maximumSize, 0, -1):

            AIndices = [i for i in range(0, len(a) - size + 1)]
            BIndices = [j for j in range(0, len(b) - size + 1)]
            print("i ", size)
            print("AIndices", AIndices)
            print("BIndices", BIndices)

            for i in AIndices:
                for j in BIndices:
                    print("i  j  ", i, j)
                    # check if a contiguous superset has already been inserted;
                    # don't insert this one in that case
                    print("a and b   ", a[i:i + size], b[j:j + size])
                    if a[i:i + size] == b[j:j + size]:
                        alreadyInserted = False
                        # take indices of equal words
                        currentAIndices = [item for item in range(i, i + size)]
                        currentBIndices = [item for item in range(j, j + size)]
                        print("current A ,B  ", currentAIndices, currentBIndices)

                        for k in commonNeighboringWords:
                            print("k ", k[0])
                            if self.is_sublist(currentAIndices, k[0]) and self.is_sublist(currentBIndices, k[1]):
                                alreadyInserted = True
                                break

                        if not alreadyInserted:
                            commonNeighboringWords.append([currentAIndices, currentBIndices])
                    print("common words", commonNeighboringWords)
        if swapped:
            for item in commonNeighboringWords:
                temp = item[0]
                item[0] = item[1]
                item[1] = temp

        return commonNeighboringWords

    '''
    creating list where each element represent relation between parent and child node
    Input: Parse result
    Output: list in form :
            (rel, parent{charStartOffset, charEndOffset, wordNumber},child{charStartOffset, charEndOffset, wordNumber})
    '''

    @staticmethod
    def dependencyTreeWithOffSets(parseResult):

        dependencies = parseResult['dependencies']
        combine_dependencies = []
        res = []
        words_param = parseResult['words']
        combine_wordsList = []
        print("dependencies length ", len(dependencies))

        if (len(dependencies)) > 1:
            print("length of dependency ", len(dependencies))
            for sublist in dependencies:
                print("sublist ", sublist)
                combine_dependencies += sublist
        else:
            combine_dependencies = dependencies[0]

        if len(words_param) > 1:
            for sublist in words_param:
                combine_wordsList += sublist
        else:
            combine_wordsList = words_param[0]
        print("combine wordlist", combine_wordsList)
        print("combine dependency ", combine_dependencies)

        for dep in combine_dependencies:

            newItem = [dep[0]]
            print("dep ", dep)

            parent = dep[1][0:dep[1].rindex("-")]

            print("parent ", parent)

            wordNumber = dep[1][dep[1].rindex("-")]
            print("dep ", dep[1])

            print("newItem ", newItem)
            for i in range(len(combine_wordsList)):
                if parent == combine_wordsList[i][0]:
                    wordNumber = str(i + 1)
                    break
                else:
                    wordNumber = "invalid"
            print("word Number ", wordNumber)

            if wordNumber.isdigit() == False:
                print("WordNumber is false")
                continue

            parent += '{' + combine_wordsList[int(wordNumber) - 1][1]['CharacterOffsetBegin'] + \
                      ' ' + combine_wordsList[int(wordNumber) - 1][1]['CharacterOffsetEnd'] + ' ' + wordNumber + '}'
            print("parent append ", parent)
            newItem.append(parent)

            child = dep[2][0:dep[2].rindex("-")]
            print("child ", child)

            wordNumber = dep[1][dep[1].rindex("-")]
            print("dep ", dep[1])

            print("newItem ", newItem)
            for i in range(len(combine_wordsList)):
                if child == combine_wordsList[i][0]:
                    wordNumber = str(i + 1)
                    break
                else:
                    wordNumber = "invalid"
            print("word Number ", wordNumber)

            if wordNumber.isdigit() == False:
                continue
            child += '{' + combine_wordsList[int(wordNumber) - 1][1]['CharacterOffsetBegin'] + \
                     ' ' + combine_wordsList[int(wordNumber) - 1][1]['CharacterOffsetEnd'] + ' ' + wordNumber + '}'
            newItem.append(child)
            print(child)

            res.append(newItem)
        print(res)
        return res

    '''
    Input: output from dependencytreewithoffset i.e dependency tree, word number, word
    Output: list of relation and parent
    '''

    @staticmethod
    def findParents(dependencies, wordIndex, word):

        wordsWithIndices = ((int(item[2].split('{')[1].split('}')[0].split(' ')[2]),
                             item[2].split('{')[0]) for item in dependencies)
        print("word indices", wordsWithIndices)

        wordsWithIndices = list(set(wordsWithIndices))
        print("list of word indices", wordsWithIndices)
        wordsWithIndices = sorted(wordsWithIndices, key=lambda item: item[0])
        print("sorted list", wordsWithIndices)

        wordIndexPresentInList = False
        for i in wordsWithIndices:
            if i[0] == wordIndex:
                print("came here ", i[0], wordIndex)
                wordIndexPresentInList = True
                break

        parentsWithRelation = []

        if wordIndexPresentInList:
            print("entered if")
            # dependencies : [['root', 'Root{85 86 0}', 'country{28 35 5}']
            for j in dependencies:

                currentIndex = int(j[2].split('{')[1].split('}')[0].split(' ')[2])
                print("current index", currentIndex)

                if currentIndex == wordIndex:
                    # store [WordNumberOf parent, parent, relation]
                    # [0,Root, root]
                    parentsWithRelation.append([int(j[1].split('{')[1].split('}')[0].split(' ')[2]),
                                                j[1].split('{')[0], j[0]])

        # need to check for this section
        else:
            print("entered else")

            nextIndex = 0
            for i in range(len(wordsWithIndices)):
                if wordsWithIndices[i][0] > wordIndex:
                    nextIndex = wordsWithIndices[i][0]
                    break

            if nextIndex == 0:
                return []

            for i in range(len(dependencies)):
                if int(dependencies[i][2].split('{')[1].split('}')[0].split(' ')[2]) == nextIndex:
                    pos = i
                    break
            print("pos ", pos)

            for i in range(pos, len(dependencies)):
                if '_' in dependencies[i][0] and word in dependencies[i][0]:
                    print("found")
                    parent = [int(dependencies[i][1].split('{')[1].split('}')[0].split(' ')[2]),
                              dependencies[i][1].split('{')[0], dependencies[i][0]]
                    parentsWithRelation.append(parent)
                    break

        return parentsWithRelation

    '''
    Input: output from dependencytreewithoffset i.e dependency tree, word number, word
    Output: list of children
    '''

    @staticmethod
    def findChildren(dependencies, wordIndex, word):

        wordsWithIndices = ((int(item[2].split('{')[1].split('}')[0].split(' ')[2]),
                             item[2].split('{')[0]) for item in dependencies)
        print("word indices",list(wordsWithIndices))
        wordsWithIndices = list(set(wordsWithIndices))
        wordsWithIndices = sorted(wordsWithIndices, key=lambda item: item[0])
        childrenWithRelation = []

        wordIndexPresentInList = False
        for i in wordsWithIndices:
            if i[0] == wordIndex:
                wordIndexPresentInList = True
                break

        if wordIndexPresentInList:
            for j in dependencies:
                currentIndex = int(j[1].split('{')[1].split('}')[0].split(' ')[2])
                if currentIndex == wordIndex:
                    childrenWithRelation.append([int(j[2].split('{')[1].split('}')[0].split(' ')[2]),
                                                 j[2].split('{')[0], j[0]])

        # find the closest following word index which is in the list
        else:
            nextIndex = 0

            for i in range(len(wordsWithIndices)):
                if wordsWithIndices[i][0] > wordIndex:
                    nextIndex = wordsWithIndices[i][0]
                    break

            if nextIndex == 0:
                return []

            for i in range(len(dependencies)):
                if int(dependencies[i][2].split('{')[1].split('}')[0].split(' ')[2]) == nextIndex:
                    pos = i
                    break

            for i in range(pos, len(dependencies)):
                if '_' in dependencies[i][0] and word in dependencies[i][0]:
                    child = [int(dependencies[i][2].split('{')[1].split('}')[0].split(' ')[2]),
                             dependencies[i][2].split('{')[0], dependencies[i][0]]
                    childrenWithRelation.append(child)
                    break

        return childrenWithRelation

    '''
    Input: parse result, wordindex, leftspan tree, rightspan tree
    Output: list containing infromation about particular word index
             [wordIndices, lemmas, wordIndex - startWordIndex, endWordIndex - wordIndex]
    '''
    @staticmethod
    def findNeighborhoodSimilarities(sentenceDetails, wordIndex, leftSpan, rightSpan):

        lemmas = []
        wordIndices = []
        sentenceLen = len(sentenceDetails)
        startWordIndex = max(1, wordIndex - rightSpan)
        endWordIndex = min(sentenceLen, wordIndex + rightSpan)
        for item in sentenceDetails[startWordIndex - 1:wordIndex - 1]:
            if item[3] not in stopwords + punctuation_list:
                lemmas.append(item[3])
                wordIndices.append(item[1])
        for item in sentenceDetails[wordIndex:endWordIndex]:
            if item[3] not in stopwords + punctuation_list:
                lemmas.append(item[3])
                wordIndices.append(item[1])
        return [wordIndices, lemmas, wordIndex - startWordIndex, endWordIndex - wordIndex]





#u = utlity()
#t = textprocessing()
#t1 = textprocessing()
#print(u.get_commonNeighboringWords(["hello", "you", "are", "how"], ["hello", "how", "are", "you"]))
#t2 = 'it is good to here . How are you'
#x=t.parser(t2)
#y=t.parser("every thing is fine")
#print("parser ", x)
#print("get parse", y)
#print(y["dependencies"][0])
#print(u.findParents(y["dependencies"][0], 2, "word"))
#print(u.findParents([[['ROOT', 'Root-', 'good-'], ['nsubj', 'good-', 'it-'], ['cop', 'good-', 'is-'], ['nmod', 'good-', 'here-'], ['case', 'here-', 'to-'], ['punct', 'good-', '.-']], [['ROOT', 'Root-', 'How-'], ['dep', 'How-', 'are-'], ['nsubj', 'are-', 'you-']]], 1, "how"))

#print(u.findChildren(u.dependencyTreeWithOffSets(x),3,"how"))
#print(u.dependencyTreeWithOffSets({'text': ['it is good to here . How are you'], 'dependencies': [[['ROOT', 'Root-', 'good-'], ['nsubj', 'good-', 'it-'], ['cop', 'good-', 'is-'], ['nmod', 'good-', 'here-'], ['case', 'here-', 'to-'], ['punct', 'good-', '.-'], ['parataxis', 'good-', 'are-'], ['advmod', 'are-', 'How-'], ['nsubj', 'are-', 'you-']]], 'words': [[['it', {'NamedEntityTag': 'O', 'CharacterOffsetEnd': '22', 'CharacterOffsetBegin': '20', 'PartOfSpeech': 'PRP', 'Lemma': 'it'}], ['is', {'NamedEntityTag': 'O', 'CharacterOffsetEnd': '25', 'CharacterOffsetBegin': '23', 'PartOfSpeech': 'VBZ', 'Lemma': 'be'}], ['good', {'NamedEntityTag': 'O', 'CharacterOffsetEnd': '30', 'CharacterOffsetBegin': '26', 'PartOfSpeech': 'JJ', 'Lemma': 'good'}], ['to', {'NamedEntityTag': 'O', 'CharacterOffsetEnd': '33', 'CharacterOffsetBegin': '31', 'PartOfSpeech': 'TO', 'Lemma': 'to'}], ['here', {'NamedEntityTag': 'O', 'CharacterOffsetEnd': '38', 'CharacterOffsetBegin': '34', 'PartOfSpeech': 'RB', 'Lemma': 'here'}], ['.', {'NamedEntityTag': 'O', 'CharacterOffsetEnd': '40', 'CharacterOffsetBegin': '39', 'PartOfSpeech': '.', 'Lemma': '.'}], ['How', {'NamedEntityTag': 'O', 'CharacterOffsetEnd': '44', 'CharacterOffsetBegin': '41', 'PartOfSpeech': 'WRB', 'Lemma': 'how'}], ['are', {'NamedEntityTag': 'O', 'CharacterOffsetEnd': '48', 'CharacterOffsetBegin': '45', 'PartOfSpeech': 'VBP', 'Lemma': 'be'}], ['you', {'NamedEntityTag': 'O', 'CharacterOffsetEnd': '52', 'CharacterOffsetBegin': '49', 'PartOfSpeech': 'PRP', 'Lemma': 'you'}]]]}))
