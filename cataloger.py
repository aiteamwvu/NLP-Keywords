from newspaper import Article
from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://aiwvu.ml", auth=basic_auth("neo4j", "edupassword"))


session = driver.session()

def batchKeys():
   result = driver.session().run("match (a:Article {keywordProcessed : false}) WHERE a.source_content <> 'video' RETURN a.link AS url LIMIT 20")
   for record in result:
      processKeys(record['url'])

def processKeys(url):
   try:
      print(url)
      art = Article(url)
      art.download()
      art.parse()
      art.nlp() #need to use custom keyword extractor here
      print('keys' + str(art.keywords))
      request = "MATCH (a:Article { link : '{url}' } ) SET a.keywordProcessed = true FOREACH ( key IN {keywords} | MERGE (b:Keyword {name : key})  MERGE (a)-[:Has]->(b) )"
      request = request.replace('{url}', url)
      request = request.replace("{keywords}", str(art.keywords))
      print(request)        
      driver.session().run(request)
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
   batchKeys()
   
   
     
