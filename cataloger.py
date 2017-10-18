from newspaper import Article
from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("http://aiwvu.ml:7474", auth=basic_auth("neo4j", "edupassword"))
session = driver.session()

def batchKeys():
   result = driver.session().run("match (a:Article {keywordProcessed : false}) RETURN a.link AS url LIMIT 10")
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


   
if __name__ == '__main__':
   batchKeys(driver)
   while True:
      try:
         dbAdd( input("Url>"))
      except EOFError:
         break;
   
   
     
