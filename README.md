# NLP-Keywords
Keyword extraction from text

To Run:
Install nltk: http://www.nltk.org/install.html
Install rake-nltk: https://pypi.python.org/pypi/rake-nltk

import file to where used and call the getKeywords function.

It will take 2 parameters: text, numOfKeywords
text is a large string to extract keywords from.
numOfKeywords is the number of keywords you want returned.

It will return a dictionary.
It will be consisted of keywords and normalized weights (the weight is normalized for the size of the text)
The words are the key to find weights.

NOTE: if numOfKeywords is higher than the number of keywords available, it will return everything it can
