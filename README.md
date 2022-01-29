# Short Answer Grader 
Computers routinely grade multiple-choice questions by simply matching them to an answer key. Can they effectively score in exams? This report examines an automated technique for grading short answer responses, using a grading system. This system assigns a grade to a student answer based on its similarity to a model answer provided by an instructor. Similarity is measured using 
- The semantic similarity between isolated words, and 
- The similarity between the order of those words. 
The performance of the system was evaluated by scoring actual exam questions and comparing the computer-assigned grades to those given by human instructors. In favourable situations, the correlation between the computer and the human-assigned grades was only a little less than between human instructors. Several characteristics of texts can cause the performance of the system to degrade. For example, the system's performance is poor with answers that contain negations, truly unique phrases or idioms, misspelled words, or contradictory information.

The below model explains how answer are evaluated going through different Phases. 

![pipeline for model](https://github.com/shashwat-code/Short-Answer-Grader/blob/main/model%20pipeline%20for%20evaluation.png?raw=true)

## 
## PPDB
To get synonyms of words paraphrase database is used .
Which under different sizes (Used XXXL)

[PPDB download link](http://paraphrase.org/#/download)


## Model to check word similarity
![word similarity](https://github.com/shashwat-code/Short-Answer-Grader/blob/main/model%20of%20word%20alignment.png?raw=true)

##
## Comparsion between different Models Used:

Figure shows the grade for 500 students from Pre Trained Model where every point represents a student Id corresponding to which grades are provided by model 2
![pipeline for model](https://github.com/shashwat-code/Short-Answer-Grader/blob/main/comparsion%20between%20ridge%20and%20perceptron%20model.png?raw=true)


## Dataset

We have used dataset provided by Rada Mihalcea who is professor at University of Michigan.This data set consists of ten assignments with between four and seven questions each and two exams with ten questions each. These assignments/exams were assigned to an introductory computer science class at the University of North Texas. The
data is in plaintext format. Each assignment includes the question, instructor answer, and set of student answers with the average grades of two human teacher included. Both teacher were asked to grade for correctness on an integer scale from 0 to 5.

[Dataset Download link](https://web.eecs.umich.edu/~mihalcea/downloads.html)
## Tech Stack

**IDE:** Jupyter Notebook , PyCharam

**Language:**  python

**Libraries Used:** numpy, Spacy, Scikit Learn




## References

- [aclweb.org(S15-2027)](https://www.aclweb.org/anthology/S15-2027.pdf)
- [mitpressjournals](https://www.mitpressjournals.org/doi/abs/10.1162/tacl_a_00178)
- [aclweb.org(N16-1123)](https://www.aclweb.org/anthology/N16-1123.pdf)
- [towardsdatascience](www.towardsdatascience.com)
- [analyticsvidhya](www.analyticsvidhya.com)
- [text-similarities-da019229c894](https://medium.com/@adriensieg/text-similarities-da019229c894)
- [sentence-similarity](https://nlp.town/blog/sentence-similarity/)
- [ejournals.bc.edu](https://ejournals.bc.edu/index.php/jtla/article/view/1668)
- [automated-essay-grading](https://medium.com/@ishitatiwari625/automated-essay-grading-254589d80949)
- [natural-language-processing](https://medium.com/@ageitgey/natural-language-processing-is-fun-9a0bff37854e)
- [introduction-to-stanfordnlp-an-nlp-library](https://medium.com/analytics-vidhya/introduction-to-stanfordnlp-an-nlp-library-for-53-languages-with-python-code-d7c3efdca118)
- [Stemming](https://www.nltk.org/howto/stem.html)
- [Scipy](https://www.scipy.org)



