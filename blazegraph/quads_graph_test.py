import urllib
import httplib2
import simplejson
from rdflib.plugin import register, Parser, Serializer

register('json-ld', Parser, 'rdflib_jsonld.parser', 'JsonLDParser')
register('json-ld', Serializer, 'rdflib_jsonld.serializer', 'JsonLDSerializer')
from rdflib import Graph, Literal, URIRef, Dataset

endpoint_fqdn = 'http://'
endpoint_port = '30000'
graph_namespace = 'demo_quads'
graph_uri = endpoint_fqdn + ':' + endpoint_port + '/blazegraph/namespace/'+ graph_namespace + '/sparql'
print(graph_uri)

uri = graph_uri + '?' + 'query=CONSTRUCT { ?s ?p ?o } WHERE { graph ?g { hint:Query hint:constructDistinctSPO false . ?s ?p ?o } }'

test_json = """{
          "@graph": [
            {
              "@id": "_:genid1",
              "@type": "http://www.w3.org/2002/07/owl#Axiom",
              "http://purl.org/dc/elements/1.1/type": [
                {
                  "@id": "http://purl.obolibrary.org/obo/ECO_0007636"
                },
                {
                  "@id": "http://purl.obolibrary.org/obo/ECO_0007638"
                },
                {
                  "@id": "http://purl.obolibrary.org/obo/ECO_0007645"
                }
              ],
              "http://www.geneontology.org/formats/oboInOwl#hasDbXref": [
                "url:http://en.wikipedia.org/wiki/Hemangiosarcoma",
                "url:https://en.wikipedia.org/wiki/Angiosarcoma",
                "url:https://ncit.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=C3088",
                "url:https://www.ncbi.nlm.nih.gov/pubmed/23327728"
              ],
              "http://www.w3.org/2002/07/owl#annotatedProperty": {
                "@id": "http://purl.obolibrary.org/obo/IAO_0000115"
              },
              "http://www.w3.org/2002/07/owl#annotatedSource": {
                "@id": "http://purl.obolibrary.org/obo/DOID_0001816"
              },
              "http://www.w3.org/2002/07/owl#annotatedTarget": "A vascular cancer that derives_from the cells that line the walls of blood vessels or lymphatic vessels."
            },
            {
              "@id": "_:genid10",
              "@type": "http://www.w3.org/2002/07/owl#Axiom",
              "http://purl.org/dc/elements/1.1/type": {
                "@id": "http://purl.obolibrary.org/obo/ECO_0007638"
              },
              "http://www.geneontology.org/formats/oboInOwl#hasDbXref": "url:http://en.wikipedia.org/wiki/Lambert%E2%80%93Eaton_myasthenic_syndrome",
              "http://www.w3.org/2002/07/owl#annotatedProperty": {
                "@id": "http://purl.obolibrary.org/obo/IAO_0000115"
              },
              "http://www.w3.org/2002/07/owl#annotatedSource": {
                "@id": "http://purl.obolibrary.org/obo/DOID_0050214"
              },
              "http://www.w3.org/2002/07/owl#annotatedTarget": "A neuromuscular junction disease that is characterized by an abnormality of acetylcholine (ACh) release at the neuromuscular junction which results from an autoimmune attack against voltage-gated calcium channels (VGCC) on the presynaptic motor nerve terminal."
            }]
        }"""

graph = Graph().parse(data=test_json, format='json-ld')

h = httplib2.Http()
graph_triples = graph.serialize(format='json-ld')

resp, content = h.request(uri,method = 'PUT', body = graph_triples,headers = {'content-type': 'application/ld+json'})
print(resp)

dset = Dataset()
dset.default_context.parse(data=test_json, format="application/ld+json")
print("graph (%s) contains %s triples " % (dset.identifier, len(dset.default_context)))
