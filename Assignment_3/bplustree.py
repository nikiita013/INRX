# -*- coding: utf-8 -*-
import math 

import sys

class Link:
    def __init__(self, value):
        self.left = None
        self.value = value
        self.right = None
    
class Node:
    def __init__(self, t = False):
        self.container = []
        self.leaf = t
        self.parent = None
        self.next = None
        pass
    
class Tree:
    def __init__(self, m):
        self.keys = m-1
        self.root = None
    
    
    def insert(self, link, leaf, node):
        #SEARCH and get the node ref
        #node = self.search(val, self.root)
        #search among the node vals
        #if size less than order then insert
        #else break into 2 halves and pass the link to parent
        if node == None:
            self.root = Node(leaf)
            self.root.container.append(link)
            return self.root
            
        if len(node.container) < self.keys:
            #link.right = node.container[len(node.container)-1].right
            node.container[len(node.container)-1].right = link.left
            node.container.append(link)
            return node
        
        m = int(math.ceil(self.keys/2.0))
        
        leftl = Node(leaf)
        rightl = Node(leaf)
        
        for i in range(m):
            leftl.container.append(node.container[i])
            
        if leaf == True:
            for i in range(m, self.keys):
                rightl.container.append(node.container[i])
            rightl.container.append(link)
            midlink = Link(node.container[m].value)
            
        else:
            for i in range(m+1, self.keys):
                rightl.container.append(node.container[i])
            rightl.container.append(link)
            midlink = node.container[m]
        node.next = rightl
        del node.container[:]
        for i in range(len(leftl.container)):
            node.container.append(leftl.container[i])
            
        midlink.left = node
        midlink.right = rightl
        par = self.insert(midlink, False, node.parent)
        node.parent = par
        rightl.parent = par
        del leftl
        return rightl
        
    def search(self, word, node):
        if node == None:
            return None
            
        temp = False
        if node.leaf == True:
            #print "Yahoo"
            return node
        #print "SAD"
        for n in node.container:
            #print word," < ",n.value
            if word < n.value:
                #print "YES IN"
                temp = True
                ref = self.search(word, n.left)
                break
        if temp == False:
            ref = self.search(word, n.right)
        
        return ref
        
    def searchE(self, word):
        t = self.search(word, self.root)
        if t == None:
            return None
        else:
            temp = True
            candidates = []
            temp2 = False
            while t != None and temp == True:
                for i in range(len(t.container)):
                    #print t.container[i].value
                    if word in t.container[i].value:
                        candidates.append(t.container[i].value)
                        temp2 = True
                    elif temp2 == True:
                        temp = False
                        break
                    else:
                        pass                       
                #if temp == True:    
                t = t.next
                    #k = 0
                """
            temp = True
            while t != None and temp == True:
                for j in range(k, len(t.container)):
                    #print "hihi ",t.container[j].value
                    if word in t.container[j].value:
                        
                    else:
                        temp = False
                        break
                t = t.next
                k = 0 """
            return candidates
            
    def traverse(self, node):
        if node == None:
            return
        
        for n in node.container:
            self.traverse(n.left)
            print n.value," ",node.leaf
        if node.leaf == False:
            self.traverse(n.right)
    
    def checklist(self, word):
        t = self.search(word, self.root)
        if t == None:
            return None
        else:
            container = []
            while t != None:
                for i in range(len(t.container)):
                    container.append(t.container[i].value)
                    #print t.container[i].value
                        #print i
                t = t.next
                #print "t: ",t
            return container
            
if __name__ == '__main__':
    t = Tree(4)
    a = 1
    #while(a != 0):
    liss = ["nik", "niki", "nok", "lik", "sans", "pra", "srid"]
    liss = sorted(liss)
    for a in liss: 
        #a = input("Enter number: ")
        node = t.search(a, t.root)
        link = Link(a)
        t.insert(link, True, node)
        
    #t.traverse(t.root)
    #print (t.searchE("pr"))
    print (t.checklist("pr"))
    
    
    
        
        
    