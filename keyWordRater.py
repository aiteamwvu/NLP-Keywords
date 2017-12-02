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


def rateSomeKeys():
    """
    Creates an interactive session for rating keywords
    Intended to get gut reaction for training an AI keyword selector    
    1 - Generic word of no importance
    2 - Normalish keyword
    3 - Very good keyword
    """
    result = driver.session().run("match (k:Keyword) WHERE not 'rating' in keys(k) RETURN k.name AS name ")
    for entry in result:
        keyname = entry['name']
        rating = input( keyname + ' rating?')
        driver.session().run("MATCH (k:Keyword {name : $keyname} ) SET k.rating = $rating", keyname=keyname, rating=rating)
   


if __name__ == "__main__":
   rateSomeKeys()
