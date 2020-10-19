import pandas as pd
import numpy as np
from io import StringIO
# %matplotlib inline
from rdflib import Graph,URIRef
from gastrodon import LocalEndpoint,one,QName
pd.set_option("display.width",100)
pd.set_option("display.max_colwidth",80)
import statistics


input_path = "/home/jovyan/semantics-information-broker/"

f_dbp_onto = input_path + "DBpedia ontology 2016/" + "dbpedia_2016-10.nt"
f_dbp_people = input_path + "DBpedia_people/DBpedia_people_no-semantics/" + "goldStandard_dbp_cleaned.nt"
f_disease = input_path + "Diseases/no-semantics/" + "goldStandard_diseases.nt"

dbpedia_ontology = Graph()
dbpedia_ontology.parse(f_dbp_onto, format="nt")
dbpedia_People = Graph()
dbpedia_People.parse(f_dbp_people, format="nt")
disease_ICD = Graph()
disease_ICD.parse(f_disease, format="nt")

print(len(dbpedia_ontology))
print(len(dbpedia_People))
print(len(disease_ICD))

dbp_p=LocalEndpoint(dbpedia_People)
drug=LocalEndpoint(disease_ICD)
dbp_onto=LocalEndpoint(dbpedia_ontology)

subject=dbp_p.select("""
   SELECT ?s (COUNT(*) AS ?count) {
      ?s ?p ?o .
      
   } GROUP BY ?s ORDER BY DESC(?count)
""")

properties=dbp_p.select("""
   SELECT ?p (COUNT(*) AS ?count) {
      ?s ?p ?o .
      
   } GROUP BY ?p ORDER BY DESC(?count)
""")

obj = dbp_p.select("""
   SELECT ?o (COUNT(*) AS ?count) {
      ?s ?p ?o .
      
   } GROUP BY ?o ORDER BY DESC(?count)
""")

