# NLP-Keywords
Keyword extraction from text

To Run with Python 2:

Install nltk: http://www.nltk.org/install.html

Install rake-nltk: https://pypi.python.org/pypi/rake-nltk

(If using Python 3, just use "pip3 install rake-nltk")

------------------
import file to where used and call the getKeywords function.

------------------
It will take 3 parameters: text, numOfKeywords, title.

text is a large string to extract keywords from.

numOfKeywords is the number of keywords you want returned.

title is an optional parameter and can be skipped if unavailable but it can increase the accuracy of the keywords.

------------------
It will return a dictionary.

It will be consisted of keywords and normalized weights (the weight is normalized for the size of the text).

The words are the key to find weights.

------------------
NOTE: if numOfKeywords is higher than the number of keywords available, it will return everything it can.


------------------
install keyWordRating:

Using your favorite flavor of pip, install neo4j-driver

Modding:

If you want to rate keywords indefinitely, delete 'LIMIT X' from the query.

Rating guide:
1 Bad/generic keyword
2 normal keyword
3 good/descriptive/useful keyword

Don't sweat it too much if you feel like you made a mistake. You can always go to 
35.197.88.141:7474

to override an old rating. edupassword is the password. 

