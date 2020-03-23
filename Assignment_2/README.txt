_______________________________________________README____________________________________________________
---------------------------------INFORMATION RETRIEVAL (ASSIGNMENT 2)------------------------------------
------------------------------SUBMITTED BY - NIKITA AGARWAL (ISM2013016)---------------------------------
____________________________________________IIIT ALLAHABAD_______________________________________________
IN IS THE FOLLOWUP ASSIGNMENT OF FIRST ONE. IN THIS SPELLING CORRECTION HAS BEEN IMPLEMENTED:

STEPS:
1) RECEIVE QUERY FROM THE QUERY INPUT FILE
2) DO PRUNING AND STEMING
3) CALCULATE THE JAQUARD COEFFICIENT OF QUERY WORDS FOR ALL WORDS IN DICTIONARY
4) SORT AND CHECK FOR THE ONES ABOVE THRESHOLD
5) IF THERE ARE SOME ABOVE THRESHOLD THEN CONSIDER THOSE OTHERWISE IF NONE THEN CONSIDER THE TOP 10 WORDS
6) CALCULATE THE EDIT DISTANCE FOR SELECTED IN STEP 5
7) FOR MIN EDIT DISTANCE WORDS GET THEIR CORRESPONDING ORIGINAL WORD AND THEN AGAIN CALCULATE EDIT DISTANCE
8) DISPLAY THE WORDS WITH MIN EDIT DISTANCES

NOTE: HERE THRESHOLD HAS BEEN CONSIDERED AS 0.5
 
IN THE FOLDER THERE ARE FOLLOWING FILES:

1) queryEN.txt : It contains all the unique words from the english corpus and their correspnding 
    frequency in the corpus.
    
2) queryHIN.txt : It contains all the unique words from the hindi corpus and their correspnding 
    frequency in the corpus.

3) enassign2.py: It is the python code for english task. 

4) hinassign2.py: It is the python code for hindi task. 

5) Dand_Prakriya.xlsx : It is the given corpus for the assignment.


PRE-REQUISITES:
1) PYTHON 2.7
2) INSTALL PYCPARSER https://github.com/eliben/pycparser
3) PYTHON PACKAGES: xlrd, editdistance


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


