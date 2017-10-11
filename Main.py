from newspaper import Article
from rake_nltk import Rake

# parameters are as follows:
# text (string: text to obtain keywords from)
# numOfKeywords (integer: how many keywords to obtain from text)
def getKeywords(text, numOfKeywords):

    # clean keywords; some keywords from rake have junk in them
    # parameters are as follows:
    # words (list of strings: words to scrub of junk data and irrelevant data)
    def scrubWord(word):
        word = word.replace(",", "")
        word = word.replace(".", "")
        return word
    rak = Rake()  # english by default

    # extract keywords and store them+their degree in a dictionary
    rak.extract_keywords_from_text(text)
    wordDic = rak.get_word_degrees()

    rankedWords = sorted(wordDic, key=wordDic.get, reverse=True)
    # remove words which are not valid keywords or are not useful
    invalidWords = [u'\u201d', u'\u201c', u'\u2019', u'\u2018', u'\u2014']
    rankedWords = [word for word in rankedWords if word not in invalidWords]
    rankedWords = scrubList(rankedWords)
    returnDic = {}

    if (numOfKeywords > len(rankedWords)):
        numOfKeywords = len(rankedWords)

    for it in range(0, numOfKeywords):
        temp = rankedWords[it]
        temp = scrubWord(temp) # scrub the word to be stored without changing it's value in the list

        #add the new, scrubbed word and it's weight
        returnDic[temp.encode('UTF8')] = (wordDic[rankedWords[it]] * (1.0/len(wordDic)))

    return returnDic

if __name__ == '__main__':
   url = 'https://techcrunch.com/2017/10/06/apple-is-looking-into-reports-of-iphone-8-batteries-swelling/'
   
   # newspaper
   art = Article(url, language='en')  # English
   art.download()
   art.parse()
   print(getKeywords(art.text, 10))
   art.nlp();
   
   #note art.keywords, art.title
   print(art.keywords);
