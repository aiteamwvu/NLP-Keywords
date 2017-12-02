# NLP-Keywords

## Contents

* Main and Main3

Modules for extracting keywords from text documents, presumably from Newspaper

* cataloger

Utility for forming a semantic network. Adds specified articles
to the neo4j database, along with keywords and related nodes.


* keyWordRater

Utility for rating keywords to create training data.


##Main and Main3


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



##cataloger

###API

* batchKeys()
 * Adds keywords to unlabled articles in the neo4j database. No Return.
 * Deletes articles with broken links.
 * Bug: If a video or other non-text media is labeled as an Article, it gets deleted rather than relabeled. 


* dbAdd(url, keyDict=None)
  * Adds the keywords to the article corresponding to the url
  * If the article doesn't exist, creates one.
  * keyDict - A dictionary of keywords and their corresponding certainty
    * Each key should be a string, and each value should be a number
    * By default, populated using Main3's keyword algorithm
  * Throws ArticleException and UnicodeDecodeErrror based off of keyword and article content

* dbSearch(searchString)
  * Returns articles whose keywords appear in the search string
  * See neo4j bolt format for articles structure

## keyWordRater
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

