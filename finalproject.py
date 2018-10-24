
from math import log

class TextModel:
    """a data type as a blueprint for objects that model a body of text
    """
    def __init__(self, model_name):
        """a constructor of a TextModel object
        """
        self.name = model_name
        self.words = {}            # word frequencies
        self.word_lengths = {}     # word lengths frequncies
        self.stems = {}            # stem frequencies
        self.sentence_lengths = {} # sentence lengths frequencies
        self.punctuations = {}     # punctuations
        
    def __repr__(self):
        """Return a string representation of the TextModel.
        """
        s = '  text model name: ' + self.name + '\n'
        s += '    number of words: ' + str(len(self.words)) + '\n'
        s += '    number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '    number of stems: ' + str(len(self.stems)) + '\n'
        s += '    number of sentence lenths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '    number of punctuations: ' + str(len(self.punctuations))
        return s

    def add_string(self, s):
        """adds s to the model by augmenting the feature dictionaries
           defined in the constructor
           s - a string of text
        """
        # punctuations
        letters = ' ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        for p in s:
            if p not in letters:
                if p in self.punctuations:
                    self.punctuations[p] += 1
                else:
                    self.punctuations[p] = 1
                  
        # sentence_lengths
        sent_list = s.split()
        count = 0
        for word in sent_list:
            if word[-1] == '!' or word[-1] == '?' or word[-1] == ';' or word[-1] == '.':
                count += 1
                if count in self.sentence_lengths:
                    self.sentence_lengths[count] += 1
                else:
                    self.sentence_lengths[count] = 1
                count = 0
            else:
                count += 1
                        
        word_list = clean_text(s)

        # words
        for w in word_list:
            if w in self.words:
                self.words[w] += 1
            else:
                self.words[w] = 1
                
        # word_length
        for w in word_list:
            if len(w) in self.word_lengths:
                self.word_lengths[len(w)] += 1
            else:
                self.word_lengths[len(w)] = 1
        # stem
        for w in word_list:
            w = stem(w)
            if w in self.stems:
                self.stems[w] += 1
            else:
                self.stems[w] = 1

    def add_file(self, filename):
        """adds all of the text in the file identified by filename to the model
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text = f.read()
        f.close() 
        
        self.add_string(text)

    def save_model(self):
        """saves the TextModel object self by writing its various
           feature dictionaries to files
        """
        # words
        fname_words = self.name + '_words'
        f1 = open(fname_words, 'w')      
        f1.write(str(self.words))              
        f1.close()                    
        # word_lengths
        fname_word_lengths = self.name + '_word_lengths'
        f2 = open(fname_word_lengths, 'w')      
        f2.write(str(self.word_lengths))              
        f2.close()
        # stems
        fname_stems = self.name + '_stems'
        f3 = open(fname_stems, 'w')      
        f3.write(str(self.stems))              
        f3.close()
        # sentence_lengths
        fname_sentence_lengths = self.name + '_sentence_lenghts'
        f4 = open(fname_sentence_lengths, 'w')      
        f4.write(str(self.sentence_lengths))              
        f4.close()
        # punctuations
        fname_punctuations = self.name + '_punctuations'
        f5 = open(fname_punctuations, 'w')      
        f5.write(str(self.punctuations))              
        f5.close()

        
    def read_model(self):
        """reads the stored dictionaries for the called TextModel object
           from their files and assigns them to the attributes of the called
           TextModel
        """
        # words
        fname_words = self.name + '_words'
        f1 = open(fname_words, 'r')    
        d_str_1 = f1.read()           
        f1.close()
        self.words = dict(eval(d_str_1))      
        # word_lengths
        fname_word_lengths = self.name + '_word_lengths'
        f2 = open(fname_word_lengths, 'r')    
        d_str_2 = f2.read()           
        f2.close()
        self.word_lengths = dict(eval(d_str_2))
        # stems
        fname_stems = self.name + '_stems'
        f3 = open(fname_stems, 'r')    
        d_str_3 = f3.read()           
        f3.close()       
        # sentence_lentghs
        fname_sentence_lengths = self.name + '_sentence_lengths'
        f4 = open(fname_sentence_lengths, 'r')    
        d_str_4 = f4.read()           
        f4.close()
        # punctuations
        fname_punctuations = self.name + '_punctuations'
        f5 = open(fname_punctuations, 'r')    
        d_str_5 = f5.read()           
        f5.close()

    def similarity_scores(self, other):
        """returns a list of log similarity scores measuring the similarity
           of self and other
        """
        word_score = compare_dictionaries(other.words, self.words)
        word_length_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stem_score = compare_dictionaries(other.stems, self.stems)
        sentence_length_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        punctuation_score = compare_dictionaries(other.punctuations, self.punctuations)

        score = [word_score, word_length_score, stem_score, sentence_length_score, punctuation_score]
        return score
    
    def classify(self, source1, source2):
        """determines which of source is the more likely source of self
           source1 - other source
           source2 - other source
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        for i in range(len(scores1)):
            scores1[i] = round(scores1[i], 3)
        for j in range(len(scores2)):
            scores2[j] = round(scores2[j], 3)

        print(scores1)
        print(scores2)
        
        weighted_sum1 = 10*scores1[0] + 5*scores1[1] + 7*scores1[2] + 10*scores1[3] + 5*scores1[4]
        weighted_sum2 = 10*scores2[0] + 5*scores2[1] + 7*scores2[2] + 10*scores2[3] + 5*scores2[4]

        if weighted_sum1 > weighted_sum2:
            print(str(self.name) + ' is more likely to have come from ' + str(source1.name))
        else:
            print(str(self.name) + ' is more likely to have come from ' + str(source2.name))


# Helper Functions

def clean_text(txt):
    """returns a list containing the words in txt after it has been “cleaned"
       txt - a string of text
    """
    s = txt.replace(',','').replace('.','').replace('!','').replace('?','').\
        replace(',','').replace('"','').replace(':','').replace(';','').replace('--','')
    s = s.lower().split()
    return s

def stem(s):
    """ return the stem of s
        s - a string
    """
    if s[-1] == 'e' and len(s) >= 3:        # --e
        s = s[:-1]
    elif s[-1] == 'y':                      # --y
        s = s[:-1] + 'i'
    elif s[-3:] == 'ies':                   # --ies
        s = s[:-3] + 'i'
    elif s[-3:] == 'ing' and len(s) >= 6:   # --ing
        if s[-4] == s[-5]:
            s = s[:-4]
        else:
            s = s[:-3]
    elif s[-2:] == 'ed':                    # --ed
        s = s[:-2]
    elif s[-2:] == 'es':                    # --es
        s = s[:-2]
    elif s[-2:] == 'er':                    # --er
        s = s[:-2]                  
    elif s[-2:] == 'or':                    # --or
        s = s[:-2]                   
    elif s[-1] == 's':                      # --s
        s = s[:-1]
    return s

def compare_dictionaries(d1, d2):
    """return their log similarity score
       d1 - a feature dictionary
       d2 - a feature dictionary
    """
    log_sim_score = 0
    total_num_d1 = 0
    
    for x in d1:            
        total_num_d1 += d1[x] 
    for y in d2:
        if y in d1:
            log_sim_score += d2[y] * log(d1[y]/ total_num_d1)
        else:
            log_sim_score += d2[y] * log(0.5/ total_num_d1)
            
    return log_sim_score

# tests
def run_tests():
    """test the TextModel object
    """
    # test 1
    source1 = TextModel('G.A.Henty')
    source1.add_file('G.A.Henty_source_text.txt')

    source2 = TextModel('shakespeare')
    source2.add_file('shakespeare_source_text.txt')

    new1 = TextModel('shakespeare_leaveout')
    new1.add_file('shakespeare_lv.txt')
    new1.classify(source1, source2)

    # test 2
    source3 = TextModel('The Adventures of Tom Sawyer')
    source3.add_file('marktwain_1_source_text.txt')

    source4 = TextModel('War and Peace')
    source4.add_file('leotolstoy_source_text.txt')

    new2 = TextModel('Adventures of Huckleberry Finn')
    new2.add_file('marktwain_2_source_text.txt')
    new2.classify(source3, source4)
