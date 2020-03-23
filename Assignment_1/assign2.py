# -*- coding: utf-8 -*-
from __future__ import print_function
import xlrd
import string
import sys
# पुरानी और (संहिता या अधिकारिता) 
#==============================================================================
# import re
#==============================================================================
#from nltk.stem import WordNetLemmatizer
#==============================================================================
# from nltk.stem.porter import PorterStemmer
# porter_stemmer = PorterStemmer()
# from nltk.stem.lancaster import LancasterStemmer
# lancaster_stemmer = LancasterStemmer()
#==============================================================================

sys.path.extend(['.', '..'])
from pycparser import c_parser, c_ast

class Node:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
        self.out = []
    
    #def addl():

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
#==============================================================================
#     print (left)
#     print (right)
#==============================================================================
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
    global mapo
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
    
    query = query.split()
    
    strin = string.ascii_uppercase
    strin = list(strin)
    
    j = 0
    print (query)
    for i in range(0, len(query)):
        if query[i] != u"&&" and query[i] != u"||" and query[i] != u"(" and query[i] != u")":
            mapo[strin[j]] = query[i]
            query[i] = strin[j]
            j += 1
                
    query = " ".join(query)     
   
    cond = query
    print (cond)
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
    
def isstopword(word):
    stop = [ u"के", u"का", u"एक", u"में", u"की", u"है", u"यह", u"और", u"से", u"हैं", u"को", u"पर", u"इस", u"होता", u"कि", u"जो", u"कर", u"मे", u"गया", u"करने", u"किया", u"लिये", u"अपने", u"ने", u"बनी", u"नहीं", u"तो", u"ही", u"या", u"एवं", u"दिया", u"हो", u"इसका", u"था", u"द्वारा", u"हुआ", u"तक", u"साथ", u"करना", u"वाले", u"बाद", u"लिए", u"आप", u"कुछ", u"सकते", u"किसी", u"ये", u"इसके", u"सबसे", u"इसमें", u"थे", u"दो", u"होने", u"वह", u"वे", u"करते", u"बहुत", u"कहा", u"वर्ग", u"कई", u"करें", u"होती", u"अपनी", u"उनके", u"थी", u"यदि", u"हुई", u"जा", u"ना", u"इसे", u"कहते", u"जब", u"होते", u"कोई", u"हुए", u"व", u"न", u"अभी", u"जैसे", u"सभी", u"करता", u"उनकी", u"तरह", u"उस", u"आदि", u"कुल", u"एस", u"रहा", u"इसकी", u"सकता", u"रहे", u"उनका", u"इसी", u"रखें", u"अपना", u"पे", u"उसके" ]    
    word = unicode(word)    
    if word in stop:
        return True
    else:
        return False
def isstopwordq(word):
    stop = [ u"के", u"का", u"एक", u"में", u"की", u"है", u"यह", u"से", u"हैं", u"को", u"पर", u"इस", u"होता", u"कि", u"जो", u"कर", u"मे", u"गया", u"करने", u"किया", u"लिये", u"अपने", u"ने", u"बनी", u"तो", u"ही", u"एवं", u"दिया", u"हो", u"इसका", u"था", u"द्वारा", u"हुआ", u"तक", u"साथ", u"करना", u"वाले", u"बाद", u"लिए", u"आप", u"कुछ", u"सकते", u"किसी", u"ये", u"इसके", u"सबसे", u"इसमें", u"थे", u"दो", u"होने", u"वह", u"वे", u"करते", u"बहुत", u"कहा", u"वर्ग", u"कई", u"करें", u"होती", u"अपनी", u"उनके", u"थी", u"यदि", u"हुई", u"जा", u"ना", u"इसे", u"कहते", u"जब", u"होते", u"कोई", u"हुए", u"व", u"न", u"अभी", u"जैसे", u"सभी", u"करता", u"उनकी", u"तरह", u"उस", u"आदि", u"कुल", u"एस", u"रहा", u"इसकी", u"सकता", u"रहे", u"उनका", u"इसी", u"रखें", u"अपना", u"पे", u"उसके" ]
    word = unicode(word)    
    if word in stop:
        return True
    else:
        return False
        
def preprocess(word):
    punc = ",.<>?:;{}[]_-=+|!`~@#$%^&*()\"\'\\/1234567890"
    for p in punc:
        word = word.replace(p, '')
    
    return word.lower()
    
def preprocessq(word):
    punc = ",.<>?:;{}[]_-=+!`~@#$%^|&*\"\'\\/1234567890"
    for p in punc:
        word = word.replace(p, '')
    word = word.replace("(", " ( ")
    
    word = word.replace(")", " ) ")
    return word.lower()
    
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
    
workbook = xlrd.open_workbook('Dand_Prakriya.xlsx')
worksheet = workbook.sheet_by_index(0)

hindict = set()
hintotal = []
i = 0
#finding all the unique words
for cell in worksheet.col_values(1):
    hintotal.append([])
    buf = cell.split()
    for word in buf:
        w = unicode(word)
#==============================================================================
#         print w
#         print isNumber(w),' ',w
#==============================================================================
        if isNumber(w) == False and hasNumbers(w) == False and isstopword(w) == False:
            temp1 = preprocess(word)
            if temp1 != "":
                hindict.add(temp1)
                hintotal[i].append(temp1)
    i += 1

for word in hindict:
    w = word.encode('utf-8')
    print (w)

freqtab = dict([ (word, 0) for word in hindict])

vectab = {}
indextab = {}
i = 0
j = 0
for cell in hintotal:
    for word in cell:
        if word in hindict:
            freqtab[word] += 1
#==============================================================================
# fptr = codecs.open("EnFreqency.txt",encoding='unicode', mode='w')
#==============================================================================

for word in hindict:
    vectab[word] = []
    indextab[word] = []
    i = 0
    for cell in hintotal:
        if word in cell:
            vectab[word].append(1)
            indextab[word].append(i)
        else:
            vectab[word].append(0)
        i += 1

#==============================================================================
# fptr = open("HinIndexTable.txt", "w")
# 
# for i in hindict:
#     i = unicode(i)
#     fptr.write(i.encode("utf-8"))
#     fptr.write(u": ")
#     for l in indextab[i]:
#         fptr.write(str(l))
#         fptr.write(", ")
#     fptr.write('\n\n')
# fptr.close() 
#==============================================================================

#sys.exit(0)
while True:
    query = raw_input("For exiting just type exit() \n Enter your query: ")
    query = query.decode('utf-8')
    if query == "exit()":
        break
    query = query.split()
    
    finalq = []
    qptr = {}
    #preprocessing the query
    for word in query:
        w = unicode(word)
        if isNumber(w) == False and hasNumbers(w) == False and isstopwordq(w) == False:
                temp = preprocessq(word)
                finalq.append(temp)
    #final keywords in finalq
                
    
    mapo = {}
    output = qp(" ".join(finalq))
    #print (finalq)
    finaldoc = []
    
    for l in output:
        finalq = []
        notq = []
        qptr = {}
        subl = l.split()
        for q in subl: 
            q = mapo[q]
            qq = q.find('!')
            if qq != -1:
                q = q.replace('!', '')
                notq.append(q)
            else:
                if q in hindict:    
                    finalq.append(q)
                    qptr[q] = 0
    
        doclist = []
        i = 0
        temp = 0
        print (finalq)
        print (notq)
        while i < len(hintotal):
            if len(finalq) == 0 and len(notq) != 0:
                for w in notq:
                    doclist = doclist + indextab[w]                
                doclist = list(set(doclist))                
                a = range(0, len(hintotal))           
                doclist = list(set(a) - set(doclist))
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
    
    finaldoc = list(set(finaldoc))
    print (finaldoc)
