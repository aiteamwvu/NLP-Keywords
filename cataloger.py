from newspaper import Article
from neo4j.v1 import GraphDatabase, basic_auth

import Main3

driver = GraphDatabase.driver("bolt://35.197.88.141:7687", auth=basic_auth("neo4j", "edupassword"))


def batchKeys():
   result = driver.session().run("match (a:Article {keywordProcessed : false}) RETURN a.link AS url")
   for record in result:
      processKeys(record['url'])

def processKeys(url):
   try:
      art = Article(url)
      art.download()
      art.parse()
      art.nlp() #need to use custom keyword extractor here
      request = "MATCH (a:Article { link : '{url}' } ) SET a.keywordProcessed = true FOREACH ( key IN {keywords} | MERGE (a)-[:Has]->(:Keyword {name : key}) )"
      driver.session().run(request, keywords=art.keywords, url=url)
      print('ding!')
   except Exception as err:
      print("Error")
      print(err)
      print(url)   
      print("")     

def dbAdd(url, keyDict=None, labels=dict()):
   if keyDict==None:
      art = Article(url)
      art = Article(url, language='en')  # English
      art.download()
      art.parse()
      keyDict = Main3.getKeywords(art.text, 10)
      labels['title'] = art.title
   #untested, but hopeful
   driver.session().run( \
   "MERGE (a:Article { link : $url } )\n" + \
   "SET a.keywordTime = timestamp()\n" + \
   "FOREACH ( key in $keyDict | MERGE (a)--[:Has]->(b:Keyword { name : key } ) SET b.value = $keyDict.key )" + \
   "FOREACH (label in $labels | SET a.label = $labels.label )", \
   keyDict=keyDict, labels=labels, url=url)


def dbSearch(searchString):
   keywords = searchString.split(" ")
   result = drive.session().run( \
   "MATCH (b:Keyword)" + \
   "WHERE b.name in $keywords" + \
   "WITH b" + \
   "MATCH (a:Article)-[h:Has]->(b)" + \
   "WITH a, sum(h.value) AS rank" + \
   "return a ORDER BY rank DESC", \
   keywords=keywords)

if __name__ == '__main__':
   dbAdd('https://techcrunch.com/2017/10/06/apple-is-looking-into-reports-of-iphone-8-batteries-swelling/')
   
   
     
