'''this file contains stopwords and punctuations which are used in python files in future'''


from nltk.corpus import stopwords
from nltk import SnowballStemmer
import codecs

para_sim = 0.9
para_dict = {}
theta = 0
punctuation_list = ['(', '-lrb-', '.', ',', '-', '?', '!', ';', '_', ':', '{', '}', '[', '/', ']', '...', '"', '\'',
                    ')', '-rrb-']
stopword_list = stopwords.words('english')
stemmer = SnowballStemmer('english')
#print(stopword_list)
file = codecs.open('/Users/shashwat/Downloads/short-answer-grader-master/Resources/ppdb-1.0-xxxl-lexical.extended.synonyms.uniquepairs', 'r')
for line in file:
    # print(line)
    if line == "/n":
        continue
    element = line.split()
    # print(element)
    para_dict[tuple(element)] = para_sim
    # print(self.para_dict)
#print(para_dict)
