# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 19:35:18 2017

@author: nikita
"""
from __future__ import print_function
import sys
sys.path.extend(['.', '..'])
from nltk.stem.snowball import SnowballStemmer
import bi    
import xlrd
import operator
import editdistance
import bplustree

stemmer = SnowballStemmer("english")
workbook = xlrd.open_workbook('Dand_Prakriya.xlsx')
worksheet = workbook.sheet_by_index(0)
#print worksheet.cell(0, 1).value
    
endict = set()
allendict = set()
entotal = []
i = 0

stemdict = {}
#finding all the unique words
for cell in worksheet.col_values(0):
    entotal.append([])
    buf = cell.split()
    for word in buf:
        w = word.encode('utf-8')
        #print isNumber(w),' ',w
        w = w.lower()
        if bi.isNumber(w) == False and bi.hasNumbers(w) == False and bi.isstopword(w) == False:
            temp1 = bi.preprocess(word.lower())
            #temp = lancaster_stemmer.stem(temp1)
            temp = "".join(stemmer.stem(temp1))
            
            
            #print (temp1, " ", temp)
            if temp != "":
                allendict.add(temp1)
                endict.add(temp)
                entotal[i].append(temp)
                if temp in stemdict.keys():
                    stemdict[temp].add(temp1)
                else:
                    stemdict[temp] = set()
                    stemdict[temp].add(temp1)
    i += 1

#==============================================================================
# bigramindex = {}
# 
# #create the bigram inverted index
# for word in endict:
#     ret = bi.createBigramF(word)
#     for w in ret:
#         if w[0] in bigramindex.keys():
#             bigramindex[w[0]].append((word, w[1]))     
#         else:
#             bigramindex[w[0]] = []
#             bigramindex[w[0]].append((word, w[1]))
#==============================================================================
   
#stemdict is the list of all the original words of the corresponding root word
   
#create  dict with the  bigrams    
allendict = sorted(allendict)
#CREATE B+ Tree
btree = bplustree.Tree(4)
for word in allendict: 
    node = btree.search(word, btree.root)
    link = bplustree.Link(word)
    btree.insert(link, True, node)
    
#btree.traverse(btree.root)
biendict = {}
for word in endict:
    biendict[word] = bi.createBigram(word)


#print (biendict)


#calculate the freaquency of the words in docs
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

#calculate the inverted index table
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

fptr = open("queryEN.txt", "r")
inp = fptr.read()
inp = inp.split("\n")
fout = open("OUT_ENGLISH.txt", "w")
for query in inp:
    if query == "":
        continue
    
    print ("Query: ",query)
    
    query = bi.spaceBrackets(query).split()
    
    originalq = []
    finalq = []
    
    #preprocessing the query
    for word in query:
        w = word.encode('utf-8')
        #print (w)
        w = w.lower()
        
        #print (w)
        
        if bi.isNumber(w) == False and bi.hasNumbers(w) == False and bi.isstopwordq(w) == False:
                temp1 = bi.preprocessq(w)
                if ("*" in temp1) and (temp1.index("*") == len(temp1)-1):
                    fout.write(temp1)
                    fout.write("\n")
                    temp1 = temp1.replace("*", "")
                    candidates = btree.searchE(temp1)
                    if candidates is not None:
                        originalq.append("(")
                        finalq.append("(")
                        #print ("yo",btree.checklist(temp1))
                        can = -1
                        for can in range(len(candidates)-1):
                            fout.write(candidates[can])
                            fout.write(" ")
                            fout.write(str(allendict.index(candidates[can])))
                            fout.write("\n")
                            originalq.append(candidates[can])
                            originalq.append("OR")
                            finalq.append("".join(stemmer.stem(candidates[can])))
                            finalq.append("OR")
                            
                        originalq.append(candidates[can+1])
                        fout.write(candidates[can+1])
                        fout.write(" ")
                        fout.write(str(allendict.index(candidates[can+1])))
                        fout.write("\n\n\n")
                        finalq.append("".join(stemmer.stem(candidates[can+1])))

                        originalq.append(")")
                        finalq.append(")")
                        
                else:
                     #print (temp1) 
                    temp = "".join(stemmer.stem(temp1))
                    #print (temp)
                    if temp == "and" or temp == "or" or temp == "not":
                        temp = temp.upper()
                        temp1 = temp1.upper()
                    #print (temp)
                    
                    originalq.append(temp1)
                    finalq.append(temp)
                    
                    
               
    #final keywords in finalq
    #print (" ".join(finalq))
    print (" ".join(originalq))
    print("\n")
    #sys.exit(0)
   # continue
    #finalq = finalq.split()
    
    cfinalq = []
    for w in finalq:
        
        if w == "AND" or w == "OR" or (w in endict) or w == "(" or w == ")" or w == "NOT":
            cfinalq.append(w)
            continue
        
        qdigram = bi.createBigram(w)
        jclist = []
        for ww in biendict.keys():
            jclist.append((ww, bi.jaquardCoeff(qdigram, biendict[ww])))
        jclist.sort(key=operator.itemgetter(1), reverse = True)
        
        #sorted(jclist.items(), key=itemgetter(1))
        checkl = []
        if jclist[0][1] >= bi.threshold:
            for ww in jclist:
                if ww[1] >= bi.threshold:
                    checkl.append((ww[0], int(editdistance.eval(w, ww[0]))))
                    #checkl.append("OR")
        else:
            for i in range(0, 10):
                checkl.append((jclist[i][0], int(editdistance.eval(w,jclist[i][0]))))
    
        checkl.sort(key=operator.itemgetter(1))
        #print (checkl)
        finall = []
        mini = 99999
        for ww in checkl:
            if ww[1] <= mini:
                mini = ww[1]
                #finall.add(ww[0])
                
                for wds in stemdict[ww[0]]:
                    #print (originalq)
                    #print (wds," ",originalq[finalq.index(w)]," ",w," ",finalq.index(w))                    
                    dd = int(editdistance.eval(originalq[finalq.index(w)], wds))
                    #print (dd)
                    finall.append((wds, ww[0] , dd, originalq[finalq.index(w)]))
            else:
                break
        
        finall.sort(key=operator.itemgetter(2))
        #print (finall)
        
        checkl = []
        finallo = []
        mini = 99999
        for ww in finall:
            if ww[2] <= mini:
                mini = ww[2]
                checkl.append(ww[1])
                checkl.append("OR")
                finallo.append(ww[0])
            else:
                break
        del checkl[-1]
        for ww in finallo:    
            print ("Did you mean this => ",ww,"? instead of this => ", originalq[finalq.index(w)])
        checkl = " ".join(checkl)     
        checkl = " ( " + checkl
        checkl = checkl + " ) "
        cfinalq.append(checkl)
    
    cfinalq = " ".join(cfinalq)
    print ("Modified Query: ",cfinalq)
    #continue
    output = bi.qp(cfinalq)
    
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
    print("Total number of documents: {}\n\n".format(len(finaldoc)))