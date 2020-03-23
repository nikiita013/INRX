# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 19:35:18 2017

@author: nikita
"""
from __future__ import print_function
import sys
sys.path.extend(['.', '..'])
from pycparser import c_parser, c_ast
from nltk.stem.snowball import SnowballStemmer

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
    print ("Before: " + query)
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
    
import xlrd
import re
#from nltk.stem import WordNetLemmatizer
#==============================================================================
# from nltk.stem.porter import PorterStemmer
# porter_stemmer = PorterStemmer()
# from nltk.stem.lancaster import LancasterStemmer
# lancaster_stemmer = LancasterStemmer()
#==============================================================================

stemmer = SnowballStemmer("english")
workbook = xlrd.open_workbook('Dand_Prakriya.xlsx')
worksheet = workbook.sheet_by_index(0)
#print worksheet.cell(0, 1).value

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
    punc = ",.<>?:;{}[]|_-=+!`~@#$%^&*\"\'\\/"
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
    
endict = set()
entotal = []
i = 0
#finding all the unique words
for cell in worksheet.col_values(0):
    entotal.append([])
    buf = cell.split()
    for word in buf:
        w = word.encode('utf-8')
        #print isNumber(w),' ',w
        w = w.lower()
        if isNumber(w) == False and hasNumbers(w) == False and isstopword(w) == False:
            temp1 = preprocess(word.lower())
            #temp = lancaster_stemmer.stem(temp1)
            temp = "".join(stemmer.stem(temp1))
            
            #print (temp1, " ", temp)
            if temp != "":
                endict.add(temp)
                entotal[i].append(temp)
    i += 1


freqtab = dict([ (word, 0) for word in endict])

vectab = {}
indextab = {}
i = 0
j = 0
for cell in entotal:
    for word in cell:
        if word in endict:
            freqtab[word] += 1
#==============================================================================
# fptr = open("EnFreqency.txt", "w")
# 
# for i in endict:   
#     fptr.write(i + ": ")
#     fptr.write(str(freqtab[i]))
#     fptr.write('\n')
# fptr.close()   
#==============================================================================
for word in endict:
    vectab[word] = []
    indextab[word] = []
    i = 0
    for cell in entotal:
        if word in cell:
            vectab[word].append(1)
            indextab[word].append(i)
        else:
            vectab[word].append(0)
        i += 1

#==============================================================================
# fptr = open("EnIndexTable.txt", "w")
# 
# for i in endict:
#     #i = unicode(i)
#     fptr.write(i.encode("utf-8"))
#     fptr.write(u": ")
#     for l in indextab[i]:
#         fptr.write(str(l))
#         fptr.write(", ")
#     fptr.write('\n\n')
# fptr.close() 
#==============================================================================
#query = "police AND officer AND cognizance OR inform"
while True:
    query = raw_input("For exiting just type exit() \n Enter your query: ")
    #query = query.decode('utf-8')
    if query == "exit()":
        break
    query = query.split()
    
    finalq = []
    
    #preprocessing the query
    for word in query:
        w = word.encode('utf-8')
        #print (w)
        w = w.lower()
            #print (w)
        if isNumber(w) == False and hasNumbers(w) == False and isstopwordq(w) == False:
                temp = preprocessq(w)
                #print (temp) 
                temp = "".join(stemmer.stem(temp))
                if temp == "and" or temp == "or" or temp == "not":
                    temp = temp.upper()
                #print (temp) 
                finalq.append(temp)
    #final keywords in finalq
    finalq = " ".join(finalq)
    
    print (finalq)
    #sys.exit(0)
    output = qp(finalq)
    
    finaldoc = []
    
    print (output)
    
    
    for l in output:
        finalq = []
        notq = []
        qptr = {}
        subl = l.split()
        for q in subl:
    
            qq = q.find('!')
            if qq != -1:
                q = q.replace('!', '')
                notq.append(q)
            else:    
                if q in endict:    
                    finalq.append(q)
                    qptr[q] = 0 
    #==============================================================================
    #     print (finalq)
    #     print (notq)
    #     sys.exit(0)
    #==============================================================================
        doclist = []
        i = 0
        temp = 0
        while i < len(entotal):
            if len(finalq) == 0 and len(notq) != 0:
                for w in notq:
                    #print (w)
                    doclist = doclist + indextab[w]
                    
                doclist = list(set(doclist))                
                #print (len(doclist))
                a = range(0, len(entotal))
                #print (len(a))
                
                doclist = list(set(a) - set(doclist))
                #print (len(doclist))
                #sys.exit(0)
                break
            
            elif len(finalq) == 0 and len(notq) == 0:
                break
            maxx = max([indextab[x][qptr[x]] for x in finalq])
           # print maxx
            for w in finalq:
                while indextab[w][qptr[w]] < maxx:
                    #print w," ",indextab[w][qptr[w]], " ",qptr[w],": ",maxx
                    if qptr[w] < len(indextab[w]) - 1:
                        qptr[w] +=  1
                    else:
                        temp = 1
                        break
                if temp == 1:
                    break
            if temp == 1:
                break
            if max([indextab[x][qptr[x]] for x in finalq]) == min([indextab[x][qptr[x]] for x in finalq]):
                w = finalq[0]
                temp1 = False
                for q in notq:
                    if maxx in indextab[q]:
                        temp1 = True
                        break
                
                if temp1 == True:
                    if qptr[w] < len(indextab[w]) - 1:
                        qptr[w] +=  1
                    else:
                        break
                    continue
                else:
                    doclist.append(maxx)
                    if qptr[w] < len(indextab[w]) - 1:
                        qptr[w] +=  1
                    else:
                        break
            i += 1
            
        finaldoc = finaldoc + doclist
    
    finaldoc = set(finaldoc)
    print (finaldoc)
    print("Total number of documents: {}".format(len(finaldoc)))