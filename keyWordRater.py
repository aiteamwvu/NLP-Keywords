from newspaper import Article
from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://35.197.88.141:7687", auth=basic_auth("neo4j", "edupassword"))


def rateSomeKeys():
   result = driver.session().run("match (k:Keyword) WHERE not 'rating' in keys(k) RETURN k.name AS name LIMIT 10")
   for entry in result:
      keyname = entry['name']
      rating = input( keyname + ' rating?')
      driver.session().run("MATCH (k:Keyword {name : $keyname} ) SET k.rating = $rating", keyname=keyname, rating=rating)
   


if __name__ == "__main__":
   rateSomeKeys()
