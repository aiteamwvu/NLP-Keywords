from newspaper import Article
from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "example"))
session = driver.session()

def getUnprocessedArticleUrls(driver):
   result = driver.session().run("match (a {processed : false}) RETURN a.url AS url")
   for record in result:
      yield record['url']

def process(driver, records):
   for url in urls:
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
      
   
if __name__ == '__main__':
   urls = getUnprocessedArticleUrls(driver)
   process(driver, urls)
   
   
     
