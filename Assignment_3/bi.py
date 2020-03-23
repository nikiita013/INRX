# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 15:26:18 2017

@author: nikita
"""
from __future__ import print_function
import sys
sys.path.extend(['.', '..'])
from pycparser import c_parser, c_ast
import string

threshold = 0.70
enthreshold = 0.50
hinthreshold = 0.33
mapo = {}

  
def spaceBrackets(query):
    query = query.replace("(", " ( ")
    query = query.replace(")", " ) ")
    return query
    
def jaquardCoeff(a, b):
    intersection = set(a) & set(b)
    union = set(a) | set(b)
    
    #print (intersection)
    #print (union)
    coeff = float(len(intersection))/float(len(union))
    #print (coeff)
    return coeff
    

def createBigramF(word):
    i = 0
    l = []
    for i in  range(0, len(word)-1):
        #print (i)
        w = word[i]
        w = w + word[i+1]
        #print (w)
        l.append(w)
    
    p = set(l)
    dic = []
    for bi in p:
        dic.append((bi, l.count(bi)))
    #print (len(p))
    print (dic)
    return dic

def createBigram(word):
    i = 0
    l = set()
    for i in  range(0, len(word)-1):
        #print (i)
        w = word[i]
        w = w + word[i+1]
        #print (w)
        l.add(w)
    
    return l
    
def ishstopword(word):
    stop = [ u"के", u"का", u"एक", u"में", u"की", u"है", u"यह", u"और", u"से", u"हैं", u"को", u"पर", u"इस", u"होता", u"कि", u"जो", u"कर", u"मे", u"गया", u"करने", u"किया", u"लिये", u"अपने", u"ने", u"बनी", u"नहीं", u"तो", u"ही", u"या", u"एवं", u"दिया", u"हो", u"इसका", u"था", u"द्वारा", u"हुआ", u"तक", u"साथ", u"करना", u"वाले", u"बाद", u"लिए", u"आप", u"कुछ", u"सकते", u"किसी", u"ये", u"इसके", u"सबसे", u"इसमें", u"थे", u"दो", u"होने", u"वह", u"वे", u"करते", u"बहुत", u"कहा", u"वर्ग", u"कई", u"करें", u"होती", u"अपनी", u"उनके", u"थी", u"यदि", u"हुई", u"जा", u"ना", u"इसे", u"कहते", u"जब", u"होते", u"कोई", u"हुए", u"व", u"न", u"अभी", u"जैसे", u"सभी", u"करता", u"उनकी", u"तरह", u"उस", u"आदि", u"कुल", u"एस", u"रहा", u"इसकी", u"सकता", u"रहे", u"उनका", u"इसी", u"रखें", u"अपना", u"पे", u"उसके" ]    
    word = unicode(word)    
    if word in stop:
        return True
    else:
        return False
def ishstopwordq(word):
    stop = [ u"के", u"का", u"एक", u"में", u"की", u"है", u"यह", u"से", u"हैं", u"को", u"पर", u"इस", u"होता", u"कि", u"जो", u"कर", u"मे", u"गया", u"करने", u"किया", u"लिये", u"अपने", u"ने", u"बनी", u"तो", u"ही", u"एवं", u"दिया", u"हो", u"इसका", u"था", u"द्वारा", u"हुआ", u"तक", u"साथ", u"करना", u"वाले", u"बाद", u"लिए", u"आप", u"कुछ", u"सकते", u"किसी", u"ये", u"इसके", u"सबसे", u"इसमें", u"थे", u"दो", u"होने", u"वह", u"वे", u"करते", u"बहुत", u"कहा", u"वर्ग", u"कई", u"करें", u"होती", u"अपनी", u"उनके", u"थी", u"यदि", u"हुई", u"जा", u"ना", u"इसे", u"कहते", u"जब", u"होते", u"कोई", u"हुए", u"व", u"न", u"अभी", u"जैसे", u"सभी", u"करता", u"उनकी", u"तरह", u"उस", u"आदि", u"कुल", u"एस", u"रहा", u"इसकी", u"सकता", u"रहे", u"उनका", u"इसी", u"रखें", u"अपना", u"पे", u"उसके" ]
    word = unicode(word)    
    if word in stop:
        return True
    else:
        return False
        
def isstopword(word):
    stop = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours	ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselve"]
    
    if word in stop:
        return True
    else:
        return False

def isstopwordq(word):
    stop = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "of", "off", "on", "once", "only", "other", "ought", "our", "ours	ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselve"]
    
    if word in stop:
        return True
    else:
        return False 
        
def preprocess(word):
    punc = ",.<>?:;{}|[]_-=+!`~@#$%^&*()\"\'\\/"
    for p in punc:
        word = word.replace(p, '') 

    return word
    
def preprocessq(word):
    punc = ",.<>?:;{}[]|_-=+!`~@#$%^&\"\'\\/"
    for p in punc:
        word = word.replace(p, '')
    
    return word
    
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)
    
def isNumber(s):
    try: 
        int(s)
        float(s)
        return True
    except ValueError:
        return False

def isassigned(word, vectab):
    try:
        vectab[word] += 0
        return False
    except KeyError:
        return True
        
class Node:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
        self.out = []

def UnaryOp(stmt):
    t = "!" + stmt.expr.name
    return t

def Traversal(root):
    left = root.left
    right = root.right
    out = root.out

    if left.__class__.__name__ == "Node":
        left = Traversal(left)
    else:
        left = [left]
        
    if right.__class__.__name__ == "Node":
        right = Traversal(right)
    else:
        right = [right]
    if root.op == "&&":
        for i in range(0, len(left)):
            for j in range(0, len(right)):
                a = left[i] + " "
                a = a + right[j]
                out.append(a)
                
    elif root.op == "||":
        for a in left:
            out.append(a)
        for a in right:
            out.append(a)     
#==============================================================================
#     print (out)
#==============================================================================
    return out
        
def BinaryOp(stmt):
    op = stmt.op
    left = stmt.left
    right = stmt.right
    
    if left.__class__.__name__ == "BinaryOp":
        left = BinaryOp(left)
    elif left.__class__.__name__ == "ID":
        left = left.name
    elif left.__class__.__name__ == "UnaryOp":
        left = UnaryOp(left)
    
    if right.__class__.__name__ == "BinaryOp":
        right = BinaryOp(right)
    elif right.__class__.__name__ == "ID":
        right = right.name
    elif right.__class__.__name__ == "UnaryOp":
        right = UnaryOp(right)
    
    n = Node(op, left, right)
    return n
    
    
def qp(query):
    query = query.replace("AND", "&&")
    query = query.replace("OR", "||")
    #print ("Before: " + query)
    query = query.split()
    
    for i in range(0, len(query)):
        #print (i)
        if query[i] == "NOT":
            #query.remove(query[i])
            i += 1
    #==============================================================================
    #         w = 
    #==============================================================================
            query[i] = "!" + query[i]
    
    query = " ".join(query)
    query = query.replace("NOT", "")
#==============================================================================
#     print (query)
#     sys.exit(0)
#==============================================================================
    cond = query
    text = r"""
               
            int main() {
                if ( """ 
    text = text + cond
    text = text +  """) {
                }
            } 
        """
    #print (text)
    
    parser = c_parser.CParser()
    ast = parser.parse(text, filename='<none>')
    #ast.show(attrnames=True, nodenames=True)
    #sys.exit(0)
    ast = ast.ext[0].body.block_items[0].cond
    if ast.__class__.__name__ == "BinaryOp":     
        root = BinaryOp(ast)
        out = Traversal(root)
    elif ast.__class__.__name__ == "UnaryOp":
        out = [UnaryOp(ast)]
    else:
        #print (ast.name)
        out = [ast.name]
    return out 

def hqp(query):
    global mapo
    #print ("original: ",query)
    query = query.replace(u"और", u"&&")
    query = query.replace(u"या", u"||")
    query = query.split()
    
    for i in range(0, len(query)):
        #print (i)
        if query[i] == u"नहीं":
            #query.remove(query[i])
            i += 1
    #==============================================================================
    #         w = 
    #==============================================================================
            query[i] = u"!" + query[i]
    
    query = " ".join(query)
    query = query.replace(u"नहीं", u"")
    #print ("replaced: ",query)
    query = query.split()
    
    strin = string.ascii_uppercase
    strin = list(strin)
    
    j = 0
    #print (query)
    for i in range(0, len(query)):
        if query[i] != u"&&" and query[i] != u"||" and query[i] != u"(" and query[i] != u")":
            mapo[strin[j]] = query[i]
            query[i] = strin[j]
            j += 1
                
    query = " ".join(query)     
   
    cond = query
    #print (cond)
    text = r"""
               
            int main() {
                if ( """ 
    text = text + cond
    text = text +  """) {
                }
            } 
        """
    #print (text)
    #print (query)
    #sys.exit(0)
    parser = c_parser.CParser()
    ast = parser.parse(text, filename='<none>')
    #ast.show(attrnames=True, nodenames=True)
    
    ast = ast.ext[0].body.block_items[0].cond
    
    if ast.__class__.__name__ == "BinaryOp":     
        root = BinaryOp(ast)
        out = Traversal(root)
    elif ast.__class__.__name__ == "UnaryOp":
        out = [UnaryOp(ast)]
    else:
        #print (ast.name)
        out = [ast.name]
    return out
