# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 18:04:34 2021
@author: Saifi
"""


import re
import random
import time, string
from typing import List

def tokenize(text: str) -> List[str]:
    """
    :param text: Takes input sentence
    :return: tokenized sentence
    """
    for punct in string.punctuation:
        text = text.replace(punct, ' '+punct+' ')
    t = text.split()
    #print("t -> tokenize", t)
    return t

def get_ngrams(n: int, tokens: list) -> list:
    """
    :param n: n-gram size
    :param tokens: tokenized sentence
    :return: list of ngrams
    ngrams of tuple form: ((previous wordS!), target word)
    """
    tokens = (n-1)*['<START>']+ tokens
    l = [(tuple([tokens[i-p-1] for p in reversed(range(n-1))]), tokens[i]) for i in range(n-1, len(tokens))]
    return l


class NgramModel(object):

    def __init__(self, n):
        self.n = n

        # dictionary that keeps list of candidate words given context
        self.context = {}

        # keeps track of how many times ngram has appeared in the text before
        self.ngram_counter = {}
        self.ngram_prob = {}
        self.voc = 0
        self.sentence = []
        self.voc_count= {}
        
        
        

    def update(self, sentence: str) -> None:
        """
        Updates Language Model
        :param sentence: input text
        """
        n = self.n
        ngrams = get_ngrams(n, tokenize(sentence))
        
        #print("ngrams -> update", ngrams)
        for ngram in ngrams:
            if ngram in self.ngram_counter:
                self.ngram_counter[ngram] += 1.0
            else:
                self.ngram_counter[ngram] = 1.0

            prev_words, target_word = ngram
            if prev_words in self.context:
                self.context[prev_words].append(target_word)
            else:
                self.context[prev_words] = [target_word]
    
    
    
    def prob(self, smooth_factor=None):
        """
        Calculates probability of a candidate token to be generated given a context
        :return: conditional probability
        """
        k=0
        
        if(smooth_factor!=None):
            k = smooth_factor
        
        
        for context,all_tokens  in self.context.items():
            for token in all_tokens:
                try:
                    count_of_token = self.ngram_counter[(context, token)]
                    count_of_context = float(len(self.context[context]))
                    result = (count_of_token + k) / (count_of_context + (k*self.voc))
                    """
                    print("context: ", context)
                    print("token: ", token)
                    print("result: ", result)
                    """

                except KeyError:
                    result = 0.0
            
                self.ngram_prob[(context,token)] = result
        return 
    
    
    
    
    
    def random_token(self, context):
        """
        Given a context we "semi-randomly" select the next word to append in a sequence
        :param context:
        :return:
        """
        r = random.random()
        map_to_probs = {}
        token_of_interest = self.context.get(context)
        #print("token: " ,token_of_interest)
        """for token in token_of_interest:
            map_to_probs[token] = self.prob(context, token)
        """   
        
        
        token_prob = {}
        
        for t in token_of_interest:
            v = self.ngram_prob[(context,t)]
            token_prob[t] = v
                
            
        
        sorted_prob = dict(sorted(token_prob.items(), key=lambda item: item[1], reverse = True))
        
        #print("first : ", list(sorted_prob.keys())[0])
        
        summ = 0
        for token in sorted_prob:
            summ += sorted_prob[token]
            if summ > r:
                return token
        
        return list(sorted_prob.keys())[0]
    
    
    
    
    

    def generate_text(self, token_count: int, context=None):
        """
        :param token_count: number of words to be produced
        :return: generated text
        """
        
        self.bulid()
        
    
        n = self.n
        queue = (n - 1) * ['<START>']
        if(context!=None):
            queue = queue + tokenize(context)
            context_queue = [queue[i] for i in range(len(queue)) if (i>= (len(queue)-n+1))]
            
        print("queue-> ",context_queue)
        
        
        
        result = [] + context.split()
        for _ in range(token_count):
            obj = self.random_token(tuple(context_queue))
            result.append(obj)
            #print(obj)
            print("queue->",context_queue, " obj -> ",obj," --->",self.ngram_prob[(tuple(context_queue),obj)])
            if n > 1:
                context_queue.pop(0)
                if obj == '.':
                
                    context_queue = (n - 1) * ['<START>']
                else:
                    context_queue.append(obj)
            print("queue-> ",context_queue)
        
        print("="*80)
        return ' '.join(result)
    
    
    
    
    def bulid(self) ->'set of unique items':
        
        for message in self.sentence:
            t = tokenize(message)
            for tm in t:
                if(tm in self.voc_count):
                    self.voc_count[tm] = self.voc_count[tm] + 1;
                else:
                    self.voc_count[tm] = 1;
        
        self.voc = len(self.voc_count)
        
        
        
        print((60 * "=="))
        print("Number of unique word of training corpus: -----------> ", self.voc) 
        print((60 * "--"))
        
        
        
        print((60 * "=="))
        print("Number of Context: ",len(self.context))
        print("Some of Context: ")
        i=0
        for k in self.context.keys() :
            if(i<20):
                print(k,"--> ",self.context[k],end=" ")
                i=i+1
            else:
                break
        print((60 * "--"))
        
        
        print((60 * "=="))
        print("n-gram count: ",len(self.ngram_counter))
        print("Some of n-gram count: ")
        i=0
        for k in dict(sorted(self.ngram_counter.items(), key=lambda item: item[1], reverse= True)) :
            if(i<50):
                print(k ,"-->",self.ngram_counter[k],end=" ")
                i=i+1
            else:
                break
        print((60 * "--"))
        
        
        
        
        self.prob(0.005)  # add-k smoothing technique is applyed, where k = 0.005
        
        
        #Probability information
        
        print((60 * "=="))
        print("Some portion of ",self.n,"-gram probability: ")
        i=0
        for k in self.ngram_prob.keys():
            if(i<20):
                print(k ,"-->",self.ngram_prob[k], end=" ")
                i=i+1
            else:
                break
        
        print((60 * "--"))
        
        print("="*80)
        
        return 

    
    


def create_ngram_model(n, path):
    m = NgramModel(n)
    with open(path, 'r') as f:
        text = f.read()

        txt = re.split(";|\.",text)

        for senten in txt:
            # add back the fullstop
            senten += '.'
            m.sentence.append(senten)
            m.update(senten)
    return m






if __name__ == "__main__":
    start = time.time()
    m = create_ngram_model(4, 'training_text.txt') # Frankenstein

    
    print (f'Language Model creating time: {time.time() - start}')
    start = time.time()
    random.seed(5)
    
    
    print(f'{"="*80}\nGenerated text:')
    print(m.generate_text(30,"Today I met"))
    print(f'{"="*80}')
    
             #it gives count of any give context
    c = 0  # turn c=1, if you want 
    while(c):
        print("check Status: ")
        print("Enter context:")
        con = list(input().split())
        print("Enter next word:")
        nxt = str(input())
        if((tuple(con),nxt) in m.ngram_counter):
            print("lob ->", m.ngram_counter[(tuple(con),nxt)])
            
        if(tuple(con) in m.context):
            print("hor -> ", len(m.context[tuple(con)]))
            
        if((tuple(con),nxt) in m.ngram_prob):
            print(m.ngram_prob[(tuple(con),nxt)])
        else:
            print("No found")
        print("if continue then enter 1, otherwise 0")
        c = int(input())
        