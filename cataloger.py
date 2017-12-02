#Needed to get clean text representations of web pages
from newspaper import Article, ArticleException

#Needed to access neo4j database
from neo4j.v1 import GraphDatabase, basic_auth

#Needed to weigh importance of keywords
import Main3

#Should be configured for wherever your neo4j db lives
graphAddressPort = "bolt://35.197.88.141:7687"
auth = basic_auth("neo4j", "edupassword")
driver = GraphDatabase.driver(graphAddressPort, auth=auth)


def batchKeys():
    """
    Adds keywords to unlabled articles in the neo4j database. No Return.
    Deletes articles with broken links.
    Bug: If a video or other non-text media is labeled as an Article, it gets deleted rather than relabeled. 
    """
    result = []
    with driver.session() as session:
        result = session.run("match (a:Article) WHERE NOT exists(a.keywordTime) RETURN a.link AS url")
        for record in result:
            print(record)
            try:
                dbAdd(record['url'])
            except UnicodeDecodeError:
                print('Unicode Error')
                session.run("match (a:Article { link : $url } ) detach delete a", url=record['url'])
            except ArticleException:
                print('Article Exception')
                session.run("match (a:Article {link : $url } ) detach delete a", url=record['url'])
          
      
   


def dbAdd(url, keyDict=None):
    """
    Adds the keywords to the article corresponding to the url
    If the article doesn't exist, creates one.
    keyDict - A dictionary of keywords and their corresponding certainty
              Each key should be a string, and each value should be a number
              By default, populated using Main3's keyword algorithm
    Throws ArticleException and UnicodeDecodeErrror based off of keyword and article content
    """
    if keyDict==None:
        art = Article(url, language='en')  # English
        art.download()
        art.parse()
        art.nlp()
        #Hybridization of newspaper and Main3's keyword extractors.
        ##newspaper picks better words, but Main3 gives a degree of certainty
        keyDict = Main3.getKeywords(art.text)
        keyDict = dict( [ (key.decode('ascii'), value) for key, value in keyDict.items() ])
        newsSet = art.keywords
        keyDict = { x : y for x, y  in keyDict.items() if x in newsSet }
    with driver.session() as session:
        session.run( \
            "MERGE (a:Article { link : $url } )\n" + \
            "SET a.keywordTime = timestamp()\n" + \
            "FOREACH ( key in keys($keyDict) |" + \
                "MERGE (k:Keyword {name : key})" + \
                "MERGE (a)-[h:Has]->(k)" + \
                "SET h.certainty = $keyDict[key])",   \
            keyDict=keyDict, url=url)

def dbSearch(searchString):
    """
    Returns articles whose keywords appear in the search string
    See neo4j bolt format for articles structure
    """
    keywords = searchString.split(" ")
    result = driver.session().run( \
        "MATCH (b:Keyword)\n" + \
        "WHERE b.name in $keywords\n" + \
        "MATCH (a:Article)-[h:Has]->(b)\n" + \
        "WITH a, sum(h.certainty) AS rank\n" + \
        "return a ORDER BY rank DESC\n", \
        keywords=keywords)
    return result;

if __name__ == '__main__':
   batchKeys()
   
   
     
