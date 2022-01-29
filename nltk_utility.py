'''
   creating parse tree  in format of
   parseResult = {'text':[], 'dependencies':[],'words':[] }
   using corenlp
'''
from nltk.tag import pos_tag
import en_core_web_sm
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.parse.corenlp import CoreNLPParser
from nltk.parse.corenlp import CoreNLPDependencyParser
import re


class textprocessing:
    def __init__(self):
        self.constituent_tree = CoreNLPParser(url='http://localhost:9000')
        self.dependency_tree = CoreNLPDependencyParser(url='http://localhost:9000')
        self.lemma = WordNetLemmatizer()
        self.ner = en_core_web_sm.load()
        self.CharacterOffsetEnd = 0
        self.CharacterOffsetBegin = 0
        self.count = 0
        self.length_of_sentence = []
        self.old = []
        self.contractions = {"'nt": "not", "'ll": " will", "'re": "are", "'ve": "have", "'m": "am"}
        self.parseResult = {'text': [], 'dependencies': [], 'words': []}

    '''
    Input: sentence
    Output: relation between words with their index
    '''

    def get_constituency_tree(self, sentence):
        sentence = sent_tokenize(sentence)
        parse_tree = ""
        t = ""
        constituent_parse = self.constituent_tree.raw_parse_sents(sentence)
        for p in constituent_parse:
            # print(p)
            for i in p:
                # print(i)
                t = str(i)
            parse_tree = ' '.join(str(t).split())
        return parse_tree

    '''
    finding dependency of sentence
    Input: Sentence
    Output: list of relation between words i.e [[rel,word1,word2],[rel,word1,word2],....] 
    '''

    def get_dependency_tree(self, sentence):
        dep_tree = []
        rel_tree = self.dependency_tree.raw_parse(sentence)
        parser = list(self.dependency_tree.raw_parse(sentence))[0]
        # print(parser)
        for k in parser.nodes.values():

            if k["head"] == 0:
                # print("k ", k)
                dep_tree.append([str(k["rel"]), "Root-", str(k["word"] + "-")])
        for dep in rel_tree:
            # print "dep ", dep.triples()
            for triple in dep.triples():
                # print("triple ", triple)
                dep_tree.append([str(triple[1]), str(triple[0][0]) + "-", str(triple[2][0]) + "-"])
        return dep_tree

    '''
    wordNet lemmatizer needs pos tag with words else it considers noun
    finding lemma of word using wordnet 
    Input: word, pos_tag[0] i.e first character of pos_tag
    Output: lemma of word
    '''

    def word_lemma(self, word, word_posTag):

        if word_posTag == 'V':
            word_lemma = self.lemma.lemmatize(word.lower(), wordnet.VERB)
            print("word lemma", word_lemma)

        elif word_posTag == 'J':
            word_lemma = self.lemma.lemmatize(word.lower(), wordnet.ADJ)
            print("word lemma", word_lemma)

        elif word_posTag == 'RB':
            word_lemma = self.lemma.lemmatize(word.lower(), wordnet.ADV)
            print("word lemma", word_lemma)

        else:
            if word == 'I':
                word_lemma = self.lemma.lemmatize(word)
            else:
                word_lemma = self.lemma.lemmatize(word.lower())
        return word_lemma

    '''
    combines all information into one 
    Input: sentence
    Output: parseResult in form of {'text': [], 'dependencies': [], 'words': []}
    '''

    def get_combine_words(self, sentence):
        print("length of sentence in get_combine ", self.length_of_sentence)
        if sentence[0] == '-':
            sentence = sentence.split('-', 1)[1]

        words_list = []
        tokenized_words = word_tokenize(sentence)
        tokenized_sentence = sent_tokenize(sentence)

        for i in tokenized_sentence:
            print("length of i ", len(i))
        print("tokenized words ", tokenized_words)

        sentence = []
        for i in tokenized_words:
            if i in self.contractions:
                sentence.append(self.contractions[i])
            else:
                sentence.append(i)
        sentence = " ".join(sentence)
        print("sentence1 ", sentence)

        tokenized_words = word_tokenize(sentence)

        posTag = pos_tag(tokenized_words)
        print("pos Tag ", posTag)
        ner = self.ner(sentence)
        print("raw ner ", ner)
        ner = ([(X.text, X.label_) for X in ner.ents])
        print("ner ", ner)
        d = [i[0] for i in ner]
        print(d)

        for i in range(len(tokenized_words)):
            if tokenized_words[i] not in d:
                ner.append((tokenized_words[i], "O"))
        print("ner ", ner)
        # if source sentence/target sentence has one sentence
        for i in range(len(tokenized_words)):
            word = tokenized_words[i]
            name_entity = ner[i]
            word_posTag = posTag[i][-1]
            if self.count == 1:
                print("word and pos_tag[0] ", word, word_posTag[0])
                word_lemma = self.word_lemma(word, posTag[0])
                print(word_lemma)
                end, begin = self.getCharOffSet(sentence, word)
                print("end and begin ", end, begin)

            else:
                # print("entered else")
                print(word_posTag)
                word_lemma = self.word_lemma(word, posTag[0])
                print(word_lemma)
                end, begin = self.getCharOffSet(sentence, word)
                print("end begin", end, begin)
                end = end + self.length_of_sentence[self.count - 2] + 1
                begin = begin + self.length_of_sentence[self.count - 2] + 1
                print("end and begin reformat ", end, begin)

            words_list.append([word, {"NamedEntityTag": str(name_entity[1]),
                                      "CharacterOffsetEnd": str(end), "CharacterOffsetBegin": str(begin),
                                      "PartOfSpeech": str(word_posTag), "Lemma": str(word_lemma)}])

        self.parseResult['text'].append(sentence)
        self.parseResult['dependencies'].append(self.get_dependency_tree(sentence))
        self.parseResult['words'].append(words_list)

        return self.parseResult

    '''
    Input: sentence
    Output: parse, tokenized sentence
    '''

    def get_parsetext(self, sentence):

        sentence = re.sub(r'([a-z]\.)([\d])', r'\1 \2', sentence)
        sentence = re.sub(r'(\)\.)([\d])', r'\1 \2', sentence)
        sentence = re.sub(r'([\d]\.)([\d])', r'\1 \2', sentence)
        sentence = re.sub(r'([a-z]\.)([A-Z])', r'\1 \2', sentence)
        sentence = re.sub(r'(\.)([A-Z]|[a-z])', r'\1 \2', sentence)
        sentence = re.sub(r'([*]|[+]|[-]|[=])([A-Z]|[a-z])', r'\1 \2', sentence)
        sentence = re.sub(r'([A-Z]|[a-z])([*]|[+]|[-]|[=])', r'\1 \2', sentence)
        sentence = re.sub(r'([*]|[+]|[-]|[=])([\d])', r'\1 \2', sentence)
        sentence = re.sub(r'([\d])([*]|[+]|[-]|[=])', r'\1 \2', sentence)
        if '[' in sentence:
            sentence = sentence.replace('[', ' [ ')
        if ']' in sentence:
            sentence = sentence.replace(']', ' ] ')
        if '/' in sentence:
            sentence = sentence.replace('/', ' / ')
        if '//' in sentence:
            sentence = sentence.replace('//', ' // ')
        if '{' in sentence:
            sentence = sentence.replace('{', ' { ')
        if '}' in sentence:
            sentence = sentence.replace('}', ' } ')
        if '(' in sentence:
            sentence = sentence.replace('(', ' ( ')
        if ')' in sentence:
            sentence = sentence.replace(')', ' ) ')
        if '$' in sentence:
            sentence = sentence.replace('$', '')
        if '\\' in sentence:
            sentence = sentence.replace('\\', ' ')
        if '|' in sentence:
            sentence = sentence.replace('|', ' ')
        if 'times' in sentence:
            sentence = sentence.replace('times', 'x')
        if 'lambda' in sentence:
            sentence = sentence.replace('lambda', ' lambda ')

        parse = {}

        tokenized_sentence = sent_tokenize(sentence)
        self.lengthofsentence(sentence)
        print("len of tokenized ", len(tokenized_sentence))
        if len(tokenized_sentence) == 1:
            self.count += 1
            for i in tokenized_sentence:
                parse = self.get_combine_words(i)
        else:
            print("inside parsetext ", self.length_of_sentence)
            for i in tokenized_sentence:
                parse = self.get_combine_words(i)
            # print(self.length_of_sentence)
        #self.length_of_sentence=[]
        return parse, tokenized_sentence

    '''
    calculating length of each individual sentence
    Input: Sentence
    Output: list of length of sentence
    '''

    def lengthofsentence(self, sentence):
        print("--------------------------------------------------88yyyyyyyyy")
        tokenized_sentence = sent_tokenize(sentence)
        print("old", self.old)
        print("tokenized_sentence",tokenized_sentence)
        if tokenized_sentence not in self.old:

            print("---------------------------------------------------------------")
            print("entered old")
            self.old.append(tokenized_sentence)

            tmp = 0
            for i in tokenized_sentence:
                self.count += 1
                s = len(i) + tmp
                self.length_of_sentence.append(s)
                tmp = s
            print("old is everything ", self.old)

    '''
    Input: Parse result
    Output: return list of [[charBegin,charEnd], wordIndex(starts from 1), word, word_POS]
    '''

    @staticmethod
    def combine_lemmaPostag(parseResult):
        res = []

        wordIndex = 1
        print("length", len(parseResult['words']))
        for i in range(len(parseResult['words'])):
            print("word i  ", parseResult['words'][i])

            for j in range(len(parseResult['words'][i])):
                print("inside word i&j ", parseResult['words'][i][j])
                tag = [[parseResult['words'][i][j][1]['CharacterOffsetBegin'],
                        parseResult['words'][i][j][1]['CharacterOffsetEnd']],
                       wordIndex, parseResult['words'][i][j][0],
                       parseResult['words'][i][j][1]['Lemma'],
                       parseResult['words'][i][j][1]['PartOfSpeech']]
                wordIndex += 1

                res.append(tag)

    '''
    Input: parse result
    Output: return list of words with valid named entity
    '''

    @staticmethod
    def nerWordAnnotator(parserResult):
        res = []
        wordIndex = 1
        for i in range(len(parserResult['words'])):
            print(len(parserResult['words']))
            for j in range(len(parserResult['words'][i])):
                print("this  ", parserResult['words'][i][j][1], parserResult['words'][i][j][0])
                tag = [[parserResult['words'][i][j][1]['CharacterOffsetBegin'],
                        parserResult['words'][i][j][1]['CharacterOffsetEnd']],
                       wordIndex, parserResult['words'][i][j][0],
                       parserResult['words'][i][j][1]['NamedEntityTag']]
                print("tag ", tag)
                wordIndex += 1
                if tag[3] != 'O':
                    res.append(tag)
        return res

    '''
    checking whether word is acronym or not
    Input: word and list of named entity
    Output: return True or False
    '''

    @staticmethod
    def is_Acronym(word, NE):
        queryWord = word.replace('.', '')
        if not queryWord.isupper() or len(queryWord) != len(NE) or queryWord.lower() in ['a', 'i']:
            return False
        acronym = True
        for i in range(len(queryWord)):
            if queryWord[i] != NE[i][0]:
                acronym = False
                break
        return acronym

    '''
       finding character offset
       Input: sentence & word
       Output: list of character end & character begin 
       '''

    @staticmethod
    def getCharOffSet(sentence, word):

        CharacterOffsetBegin = sentence.find(word)
        CharacterOffsetEnd = CharacterOffsetBegin + len(word)
        # print("begin and end word  ", word, CharacterOffsetBegin, CharacterOffsetEnd)
        return [CharacterOffsetEnd, CharacterOffsetBegin]

    '''
    clubbing named entity of same together
    Input: parse result
    Output: list of named entity
    '''

    def get_ner(self, parserResult):
        nerWordAnnotations = self.nerWordAnnotator(parserResult)
        print("word annotation ", nerWordAnnotations)
        namedEntities = []
        currentWord = []
        currentCharacterOffSets = []
        currentWordOffSets = []
        for i in range(len(nerWordAnnotations)):
            if i == 0:
                currentWord.append(nerWordAnnotations[i][2])
                currentCharacterOffSets.append(nerWordAnnotations[i][0])
                currentWordOffSets.append(nerWordAnnotations[i][1])
                if len(nerWordAnnotations) == 1:
                    namedEntities.append([currentCharacterOffSets, currentWordOffSets,
                                          currentWord, nerWordAnnotations[i - 1][3]])
                    break
                continue
            if nerWordAnnotations[i][3] == nerWordAnnotations[i - 1][3] and \
                    nerWordAnnotations[i][1] == nerWordAnnotations[i - 1][1] + 1:
                currentWord.append(nerWordAnnotations[i][2])
                currentCharacterOffSets.append(nerWordAnnotations[i][0])
                currentWordOffSets.append(nerWordAnnotations[i][1])
                if i == (len(nerWordAnnotations) - 1):
                    namedEntities.append([currentCharacterOffSets,
                                          currentWordOffSets, currentWord, nerWordAnnotations[i][3]])
            else:
                namedEntities.append([currentCharacterOffSets,
                                      currentWordOffSets, currentWord, nerWordAnnotations[i - 1][3]])
                currentWord = [nerWordAnnotations[i][2]]
                currentCharacterOffSets = []
                currentWordOffSets = []
                currentCharacterOffSets.append(nerWordAnnotations[i][0])
                currentWordOffSets.append(nerWordAnnotations[i][1])
                if i == len(nerWordAnnotations) - 1:
                    namedEntities.append([currentCharacterOffSets, currentWordOffSets,
                                          currentWord, nerWordAnnotations[i][3]])
        namedEntities = sorted(namedEntities, key=len)
        print("namedEntities ", namedEntities)
        return namedEntities

    '''
    Input: Sentence
    Output: parse Result {'text': [], 'dependencies': [], 'words': []}
    '''

    def parser(self, sentence):
        self.parseResult = {'text': [], 'dependencies': [], 'words': []}
        parseText, sentences = self.get_parsetext(sentence)
        print("sentences ", sentences)
        if len(sentences) == 1:
            return parseText
        wordOffSet = 0
        for i in range(len(parseText['text'])):
            if i > 0:
                for j in range(len(parseText['dependencies'][i])):
                    for k in range(1, 3):
                        tokens = parseText['dependencies'][i][j][k].split('-')
                        if tokens[0] == 'Root':
                            newWordIndex = 0
                        else:
                            if not tokens[len(tokens) - 1].isdigit():
                                continue
                            newWordIndex = int(tokens[len(tokens) - 1]) + wordOffSet
                        if len(tokens) == 2:
                            parseText['dependencies'][i][j][k] = tokens[0] + '-'
                        else:
                            w = ''
                            for l in range(len(tokens) - 1):
                                w += tokens[l]
                                if l < len(tokens) - 2:
                                    w += '-'
                            parseText['dependencies'][i][j][k] = w + '-'
            wordOffSet += len(parseText['words'][i])
        return parseText

textprocessing1 = textprocessing()
# print(textprocessing1.get_parsetext("Four men died in an accident"))
print((textprocessing1.get_parsetext("Four men died in an accident. he is fine ")[0]))
# print(textprocessing1.is_Acronym("UAE",[[1,2,3],2,3]))
# print(textprocessing1.parser("Four men died in an accident. he is fine "))

