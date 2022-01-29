'''working at word level finding similarity between two words as given '''

from config import *


class Similarity:
    def __init__(self):
        print("starting word_similarity file")
        self.para_dict = para_dict
        self.stemmer = stemmer

    '''
    checking if there is pair of word1 & word2 in para_dict
    Input: word1 & word2
    Output: True or False
    '''

    def check_word_present_in_dict(self, word1, word2):
        if (word1.lower(), word2.lower()) in self.para_dict:
            return True
        if (word2.lower(), word1.lower()) in self.para_dict:
            return True
        else:
            return False

    '''
    removing '.' '-' ',' from word 
    Input: word
    Output: modified word
    '''

    @staticmethod
    def modify_word(self, word):
        if len(word) > 1:
            word = word.replace('.', '')
            word = word.replace('-', '')
            word = word.replace(',', '')
        print(word)
        return word.lower()
    '''
    checking similarity between words
    steps involved:
    1.> If both words are equal then return 1
    2.> If both words have same stemma then return 1 
    3.> If both words are digits and are not equal then return 0 
    4.> If both the words are present in para_dict then return then para_sim i.e 0.9
    5.> If either of both words are present in stopwords , then return 0
    6.> If either of word is in punctuations then return 0
    '''
    def compute_word_similarity(self, word1, pos1, word2, pos2):
        new_word1 = self.modify_word(word1)
        new_word2 = self.modify_word(word2)

        print(new_word1, new_word2)

        if new_word2 == new_word1:
            return 1
        if self.stemmer.stem(new_word1) == self.stemmer.stem(new_word2):
            return 1
        if new_word2.isdigit() and new_word1.isdigit() and new_word1 != new_word2:
            return 0
        if self.check_word_present_in_dict(new_word1, new_word2):
            return para_sim
        if (new_word1 in stopword_list and new_word2 in stopword_list) or (new_word2 in stopword_list and new_word1 in stopword_list):
            return 0
        if new_word1 in punctuation_list or new_word2 in punctuation_list:
            return 0
        if pos1.lower() == 'cd' and pos2.lower() == 'cd' and (not new_word1.isdigit() and not new_word2.isdigit() and new_word1 != new_word2):
            return 0
        else:
            return 0


#s=Similarity()
#print(s.check_word_present_in_dict('fruits', '12345678'))
#s.compute_word_similarity("RESULT",23,"WORLD",34)