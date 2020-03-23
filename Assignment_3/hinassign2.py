# -*- coding: utf-8 -*-
from __future__ import print_function
import xlrd
import sys
import operator
import bi
import editdistance
import bplustree
# पुरानी और (संहिता या अधिकारिता) 
sys.path.extend(['.', '..'])
    
workbook = xlrd.open_workbook('Dand_Prakriya.xlsx')
worksheet = workbook.sheet_by_index(0)

hindict = set()
hintotal = []
allhindict = set()
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
        if bi.isNumber(w) == False and bi.hasNumbers(w) == False and bi.ishstopword(w) == False:
            temp1 = bi.preprocess(word)
            if temp1 != "":
                allhindict.add(temp1)
                hindict.add(temp1)
                hintotal[i].append(temp1)
    i += 1

allhindict = sorted(allhindict)

btree = bplustree.Tree(4)
for word in allhindict: 
    node = btree.search(word, btree.root)
    link = bplustree.Link(word)
    btree.insert(link, True, node)
 
bihindict = {}
stemdict = {}
for word in hindict:
    stemdict[word] = [word]
    bihindict[word] = bi.createBigram(word)
    #w = word.encode('utf-8')
    #print (w)

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
fptr = open("queryHIN.txt", "r")
inp = fptr.read()
inp = inp.split("\n")
fout = open("OUT_HINDI.txt", "w")
for query in inp:
    #query = raw_input("For exiting just type exit() \n Enter your query: ")
    query = query.decode('utf-8')
    if query == "":
        continue
    print ("Query: ",query)
    query = bi.spaceBrackets(query).split()
    
    originalq = []
    finalq = []
    qptr = {}
    #preprocessing the query
    for word in query:
        w = unicode(word)
       
        if bi.isNumber(w) == False and bi.hasNumbers(w) == False and bi.ishstopwordq(w) == False:
                temp1 = bi.preprocessq(word)
                if ("*" in temp1) and (temp1.index("*") == len(temp1)-1):
                    fout.write(temp1.encode("utf-8"))
                    fout.write("\n")
                    temp1 = temp1.replace("*", "")
                    candidates = btree.searchE(temp1)
                    #print (candidates[0].encode("utf-8"))
                    if candidates is not None:
                        originalq.append("(")
                        finalq.append("(")
                        #print ("yo",btree.checklist(temp1))
                        can = -1
                        for can in range(len(candidates)-1):
                            fout.write(candidates[can].encode("utf-8"))
                            fout.write(" ")
                            fout.write(str(allhindict.index(candidates[can])))
                            fout.write("\n")
                            originalq.append(candidates[can])
                            finalq.append(candidates[can])
                            originalq.append(u"या")
                            finalq.append(u"या")
                        #print ("can",can,"yoyo")    
                        finalq.append(candidates[can+1])
                        finalq.append(")")
                        originalq.append(candidates[can+1])
                        originalq.append(")")
                        fout.write(candidates[can].encode("utf-8"))
                        fout.write(" ")
                        fout.write(str(allhindict.index(candidates[can])))
                        fout.write("\n\n\n")
                else:
                    finalq.append(temp1)
                    originalq.append(temp1)
    #final keywords in finalq
    print (" ".join(originalq).encode("utf-8"))
    #sys.exit(0)
    cfinalq = []
    for w in finalq:
        if w == u"और" or w == u"या" or (w in hindict) or w == u"(" or w == u")" or w == u"नहीं":
            cfinalq.append(w)
            continue
        
        qdigram = bi.createBigram(w)
        jclist = []
        for ww in bihindict.keys():
            jclist.append((ww, bi.jaquardCoeff(qdigram, bihindict[ww])))
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
                checkl.append(u"या")
                finallo.append(ww[0])
            else:
                break
        del checkl[-1]
        for ww in finallo:    
            print ("Did you mean this => ",ww.encode('utf-8'),"? instead of this => ", originalq[finalq.index(w)].encode('utf-8'))
        checkl = " ".join(checkl)     
        checkl = u" ( " + checkl
        checkl = checkl + u" ) "
        cfinalq.append(checkl)
    
    #sys.exit(0) 
    cfinalq = " ".join(cfinalq)
    print ("Modified Query: ",cfinalq.encode('utf-8'))
    #continue
    output = bi.hqp(cfinalq)
    #print (output)
    
    finaldoc = []
    
    for l in output:
        finalq = []
        notq = []
        qptr = {}
        subl = l.split()
        for q in subl: 
            q = bi.mapo[q]
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
        #print (finalq)
        #print (notq)
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
    
    finaldoc = set(finaldoc)
    print (finaldoc)
    print("Total number of documents: {}\n\n".format(len(finaldoc)))
    
