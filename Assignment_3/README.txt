_______________________________________________README____________________________________________________
---------------------------------INFORMATION RETRIEVAL (ASSIGNMENT 3)------------------------------------
------------------------------SUBMITTED BY - NIKITA AGARWAL (ISM2013016)---------------------------------
____________________________________________IIIT ALLAHABAD_______________________________________________

A QUERY SYSTEM HAS BEEN DEVELOPED FOR DAND PRAKIYA CORPUS. IT INCLUDES THE IMPLEMENTATION TO INCLUDE THE 
TRAILING WILDCARD QUERIES.

1) enassign2.py: It is the python code for english task. 

2) hinassign2.py: It is the python code for hindi task. 

3) Dand_Prakriya.xlsx : It is the given corpus for the assignment.

4). queryEN.txt : The input file for enassign2.py

5). queryHIN.txt : The input file for hinassign2.py

6). bplustree.py : File containing B+ implementation

7). bi.py : File containing the functions used in the ain files 

NOTE: THE OUTPUT FILES OUT_ENGLISH.txt AND OUT_HINDI.txt ARE GENERATED DURING RUNTIME. IT CONTAINES THE 
WILD CARD WORDS AND THEIR CORRESPONDING VOCAB INDEXES.

PRE-REQUISITES:
1) PYTHON 2.7
2) INSTALL PYCPARSER https://github.com/eliben/pycparser
3) PYTHON PACKAGES: xlrd

_________________________________________INSTRUCTIONS TO WRITE QUERY______________________________________
--------------------------------------------FOR ENGLISH---------------------------------------------------
__________________________________________________________________________________________________________
AND, OR, NOT are the operators used for boolean query model. (NOTE: that the operators are case insensitive)

Example query1:
(Correct): Police AND officer or cognizance
(Incorrect): Police officer or cognizance (Here, there is a missing operator between police and officer)

Example query2:
(Correct): Police AND officer OR NOT cognizance
(Incorrect): Police AND officer NOT cognizance (Here, there is a missing binary operator between officer
and cognizance)

Example query3:
(Correct): Police AND (officer OR cognizance)

Example query4:
(Will give error):Police AND NOT (officer OR cognizance)
(Try modifying the input): Police AND (NOT officer AND NOT cognizance) 

Example query3:
(Correct): po* AND (offi* OR cognizance)
--------------------------------------------FOR HINDI---------------------------------------------------
__________________________________________________________________________________________________________

Everything is same as above, only thing changed are the operators:
AND => और
OR => या
NOT => नहीं

Usage is also same as above!


