from newspaper import Article
from neo4j.v1 import GraphDatabase, basic_auth

import Main3

driver = GraphDatabase.driver("bolt://35.197.88.141:7687", auth=basic_auth("neo4j", "edupassword"))


def batchKeys():
   result = driver.session().run("match (a:Article) WHERE NOT exists(a.keywordTime) RETURN a.link AS url LIMIT 3")
   for record in result:
      dbAdd(record['url'])


def dbAdd(url, keyDict=None):
   if keyDict==None:
      art = Article(url)
      art = Article(url, language='en')  # English
      art.download()
      art.parse()
      keyDict = Main3.getKeywords(art.text, 20)
      #print(keyDict)
      keyDict = dict( [ (key.decode('ascii'), value) for key, value in keyDict.items() ])
      #print(keyDict)
   #tested, now more than hopeful
   driver.session().run( \
   "MERGE (a:Article { link : $url } )\n" + \
   "SET a.keywordTime = timestamp()\n" + \
   "FOREACH ( key in keys($keyDict) | MERGE (a)-[:Has {certainty: $keyDict[key]} ]->(:Keyword {name : key})) "   \
   , keyDict=keyDict, url=url)


def dbSearch(searchString):
   keywords = searchString.split(" ")
   result = drive.session().run( \
   "MATCH (b:Keyword)" + \
   "WHERE b.name in $keywords" + \
   "WITH b" + \
   "MATCH (a:Article)-[h:Has]->(b)" + \
   "WITH a, sum(h.certainty) AS rank" + \
   "return a ORDER BY rank DESC", \
   keywords=keywords)

if __name__ == '__main__':
   batchKeys()
   
   
     
