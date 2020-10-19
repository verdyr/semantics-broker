curl -X POST http://$1:$2/blazegraph/namespace/$3/sparql --data-urlencode 'update=DROP ALL;'

curl -X POST -H 'Content-Type:application/ld+json' http://$1:$2/blazegraph/namespace/$3/sparql --data-binary '@data/test_graph.jsonld'

curl -X POST http://$1:$2/blazegraph/namespace/$3/sparql --data-urlencode 'query=SELECT * WHERE {?s ?p ?o}'
