from newspaper import Article
from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "example"))
session = driver.session()

def batchKeys(driver):
   result = driver.session().run("match (a:Article {processed : false}) RETURN a.url AS url")
   for record in result:
      process(driver, record['url'])

def processKeys(driver, url):
   try:
      print(url)
      art = Article(url)
      art.download()
      art.parse()
      art.nlp() #need to use custom keyword extractor here
      request = "MATCH (a:Article { url : $url } ) SET a.processed = true SET a.name = $title FOREACH ( key IN $keywords | MERGE (b:Keyword {name : key} ) MERGE (a)-[:Has]->(b) )"
      url.replace("'", "\\'")
      art.title = art.title.replace("'", "\\'")
      art.keywords = list(map(lambda x: x.replace("'", "\\'") , art.keywords))
      request = request.replace('$url', "'" + url + "'")
      request = request.replace('$keywords', str(art.keywords))
      request = request.replace('$title', "'" + art.title + "'")
      driver.session().run(request)
   except Exception as err:
      print("Error")
      print(err)
      print(url)            
      
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
   
   
     
