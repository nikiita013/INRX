_______________________________________________README____________________________________________________
---------------------------------INFORMATION RETRIEVAL (ASSIGNMENT 1)------------------------------------
------------------------------SUBMITTED BY - NIKITA AGARWAL (ISM2013016)---------------------------------
____________________________________________IIIT ALLAHABAD_______________________________________________

A QUERY SYSTEM HAS BEEN DEVELOPED FOR DAND PRAKIYA CORPUS. THE CORPUS HAS ENGLISH AND HINDI TEXT. QUERY 
SYSTEM HAS BEEN MADE SEPARATELY FOR BOTH THE SYSTEMS. IN THE FOLDER THERE ARE FOLLOWING FILES:

1) EnFreqency.txt : It contains all the unique words from the english corpus and their correspnding 
    frequency in the corpus.
    
2) HinFreqency.txt : It contains all the unique words from the hindi corpus and their correspnding 
    frequency in the corpus.
    
3) EnIndexTable.txt : It contains the inverted index table for unique english words. 

4) HinIndexTable.txt : It contains the inverted index table for unique hindi words.

5) assign1.py: It is the python code for english task. 

6) assign2.py: It is the python code for hindi task. 

7) Dand_Prakriya.xlsx : It is the given corpus for the assignment.


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

--------------------------------------------FOR HINDI---------------------------------------------------
__________________________________________________________________________________________________________

Everything is same as above, only thing changed are the operators:
AND => और
OR => या
NOT => नहीं

Usage is also same as above!


