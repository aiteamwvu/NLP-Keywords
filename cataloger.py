from newspaper import Article, ArticleException
from neo4j.v1 import GraphDatabase, basic_auth

import Main3

driver = GraphDatabase.driver("bolt://35.197.88.141:7687", auth=basic_auth("neo4j", "edupassword"))


def batchKeys():
   result = []
   with driver.session() as session:
      result = session.run("match (a:Article) WHERE NOT exists(a.keywordTime) RETURN a.link AS url")
   for record in result:
      print(record)
      try:
         dbAdd(record['url'])
      except UnicodeDecodeError:
          print('Unicode Error')
          with driver.session() as session:
             session.run("match (a:Article { link : $url } ) detach delete a", url=record['url'])
      except ArticleException:
          print('Article Exception')
          with driver.session() as session:
             session.run("match (a:Article {link : $url } ) detach delete a", url=record['url'])
          
      
   


def dbAdd(url, keyDict=None):
   if keyDict==None:
      art = Article(url, language='en')  # English
      art.download()
      art.parse()
      keyDict = Main3.getKeywords(art.text, 20)
      #print(keyDict)
      keyDict = dict( [ (key.decode('ascii'), value) for key, value in keyDict.items() ])
      #print(keyDict)
   #tested, now more than hopeful
   with driver.session() as session:
      session.run( \
      "MERGE (a:Article { link : $url } )\n" + \
      "SET a.keywordTime = timestamp()\n" + \
      "FOREACH ( key in keys($keyDict) | MERGE (k:Keyword {name : key}) MERGE (a)-[h:Has]->(k) SET h.certainty = $keyDict[key])"   \
      , keyDict=keyDict, url=url)


def dbSearch(searchString):
   keywords = searchString.split(" ")
   print(keywords)
   result = driver.session().run( \
   "MATCH (b:Keyword)\n" + \
   "WHERE b.name in $keywords\n" + \
   "MATCH (a:Article)-[h:Has]->(b)\n" + \
   "WITH a, sum(h.certainty) AS rank\n" + \
   "return a ORDER BY rank DESC\n", \
   keywords=keywords)

if __name__ == '__main__':
   batchKeys()
   
   
     
