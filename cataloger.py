from newspaper import Article
from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("botl://aiwvu.ml:7687", auth=basic_auth("neo4j", "edupassword"))


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

def dbAdd(url, keyDict, labels=dict()):
   #untested, but hopeful
   drive.session().run( \
   "MERGE (a:Article { link : $url } )\n" + \
   "SET a.keywordTime = timestamp()\n" + \
   "FOREACH ( key in $keyDict | MERGE (a)--[:Has]->(b:Keyword { name : key } ) SET b.value = $keyDict.key )" + \
   "FOREACH (label in $labels | SET a.label = $labels.label )", \
   keyDict=keyDict, labels=labels, url=url)

def dbAdd(url):
   art = Article(url)
   art.download()
   art.parse()
   art.nlp()
   request = "Create (a:Article { url : '{url}' } ) SET a.processed = true FOREACH ( key IN {keywords} | MERGE (b:Keyword {name : key} ) MERGE (a)-[:Has]->(b) )"
   if art.title : 
      request += "SET a.name = '" + art.title.replace("'", "\\'") + "' "
   else :
      request += "SET a.name = '" + url + "' "
   driver.session().run(request, url=url , keywords=art.keywords)

def dbSearch(searchString):
   keywords = searchString.split(" ")
   result = drive.session().run( \
   "MATCH (b:Keyword)" + \
   "WHERE b.name in $keywords" + \
   "WITH b" + \
   "MATCH (a:Article)-[h:Has]->(b)" + \
   "WITH a, sum(h.value) AS rank" + \
   "return a ORDER BY rank DESC", \
   keywords=keywords
   
if __name__ == '__main__':
   batchKeys(driver)
   
   
     
