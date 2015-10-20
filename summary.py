from __future__ import division
import re
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from string import punctuation
import sys
import os


 
class SummaryTool(object):
 
    def split_to_paragraphs(self, content):
        return content.split("\n\n")
 
    def sent_intersection(self, sent1, sent2):
 
        s1 = set(word_tokenize(sent1.lower()))
        s2 = set(word_tokenize(sent2.lower()))

        if (len(s1) + len(s2)) == 0:
            return 0
 
        return len(s1.intersection(s2)) / ((len(s1) + len(s2)) / 2)
 
    def format_sent(self, sentence):
        sentence = re.sub(r'\W+', '', sentence)
        return sentence
 
    # Convert into a dictionary <K, V>
    # K = formatted sentence
    # V = rank of the sentence
    def sentences_ranks(self, content):
 
        sentences = sent_tokenize(content)
        self._stopwords = set(stopwords.words('english') + list(punctuation))
        n = len(sentences)
        values = [[0 for x in range(n)] for x in range(n)]
        for i in range(0, n):
            for j in range(0, n):
                values[i][j] = self.sent_intersection(sentences[i],sentences[j])
 
        sentences_dic = {}
        for i in range(0, n):
            score = 0
            for j in range(0, n):
                if i == j:
                    continue
                score += values[i][j]
            sentences_dic[self.format_sent(sentences[i])] = score
        return sentences_dic
 
   
    def best_sentence(self, paragraph, sentences_dic):
 
        sentences = sent_tokenize(paragraph)

        if len(sentences) < 2:
            return ""
 
        best_sentence = ""
        max_value = 0
        for s in sentences:                                                                 
            strip_sent = self.format_sent(s)
            if strip_sent:
                if sentences_dic[strip_sent] > max_value:
                    max_value = sentences_dic[strip_sent]
                    best_sentence = s
 
        return best_sentence
 
    
    def get_summary(self, title, content, sentences_dic):
 
        
        paragraphs = self.split_to_paragraphs(content)
 
        summary = []
        summary.append(title.strip())
        summary.append("")
 
        for p in paragraphs:
            sentence = self.best_sentence(p, sentences_dic).strip()
            if sentence:
                summary.append(sentence)
 
        return ("\n").join(summary)
 
 
def main(args):
    title = args  #user query, taken from runMe
    
    value = 2                  #depending on linkFile
    for i in range(0,7):
        f = open(os.getcwd() + "//data" + "\what is biology_" + str(i) + ".txt", 'r')
        f1 = open(os.getcwd() + "//data" + "\summary" + title + str(i) + ".txt", 'w')
    #f1 = open( "processsumm.txt", 'w')
    #f = open(os.getcwd() + "//data" + "\meh.txt", 'r')   
        content = f.read()
 
        st = SummaryTool()
 
   
        sentences_dic = st.sentences_ranks(content)
 
   
        summary = st.get_summary(title, content, sentences_dic)
 
        print ("Summary for link " + str(i) + " = ")
        print(summary)
        f1.write(summary)
    
       
 
   
 
if __name__ == '__main__':
    main(sys.argv)
