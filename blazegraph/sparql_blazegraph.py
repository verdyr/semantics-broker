# Semantics Stack validation with MapR-DB table schema conversion


import locale
import rdflib
from rdflib import Graph, URIRef, Namespace, plugin
from rdflib.plugins.stores.sparqlstore import SPARQLStore
from rdflib.serializer import Serializer
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, XSD, OWL, RDF, RDFS, VOID, XMLNS
import os



#dbo = Namespace("invoice")
#
## using a Graph with the Store type string set to "SPARQLStore"
#graph = Graph("SPARQLStore", identifier="http://dbpedia.org")
#graph.open("http://HOST:PORT/blazegraph/namespace/NS_NAME/sparql")
#
#pop = graph.value(URIRef("*"), dbo.defaultGraph)
#
#print(pop)
         
# using a SPARQLStore object directly
#s = SPARQLStore(endpoint="http://dbpedia.org/sparql")
#s.open(None)
#pop = graph.value(URIRef("http://dbpedia.org/resource/Brisbane"), dbo.populationTotal)
#print("According to DBPedia, Brisbane has a population of {0:,}".format(int(pop), ",d"))                                            )


g = rdflib.Graph()

testrdf = g.load("/opt/semantics-information-broker/data/demo_triple.n3", format="n3")

g = Graph().parse(data=testrdf, format='n3')

print(g.serialize(format='json-ld', indent=4))

# the QueryProcessor knows the FOAF prefix from the graph
# which in turn knows it from reading the N3 RDF file

for row in g.query("SELECT ?s WHERE { [] foaf:knows ?s .}"):
    print(row.s)
    # or row["s"]
    # or row[rdflib.Variable("s")]

print("Initially there are {} triples in the graph".format(len(g)))


g.update(
    """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dbpedia: <http://dbpedia.org/resource/>
    INSERT
        { ?s a dbpedia:Human . }
    WHERE
        { ?s a foaf:Person . }
    """
)

print("After the UPDATE, there are {} triples in the graph".format(len(g)))

g.add((
    rdflib.URIRef("http://sib/person/serguei"),
    FOAF.givenName,
    rdflib.Literal("Serguei", datatype=XSD.string)
))


for row in g.query("SELECT ?s WHERE { [] foaf:knows ?s .}"):
        print(row.s)

print("After the UPDATE, there are {} triples in the graph".format(len(g)))




from pymantic import sparql

server = sparql.SPARQLServer('http://HOST:PORT/blazegraph/namespace/NS_NAME/sparql')

# Loading data to Blazegraph
server.update('load <file:///opt/semantics-information-broker/data/blazegraph_prefix.n3>')

# Executing query
result = server.query('select * where { <http://blazegraph.com/blazegraph> ?p ?o }')

