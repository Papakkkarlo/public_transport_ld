import rdflib
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF

PT = Namespace("http://www.semanticweb.org/user/ontologies/2019/4/untitled-ontology-42#")
GEORSS = Namespace("http://www.georss.org/georss/")

KB_path = "data/public_transport_KB"
g = Graph()
g.parse(KB_path, format="turtle")

type = 'bus'
res = g.query(
			"""SELECT ?name ?line
			   WHERE {
					?rout rdf:type pt:rout .
					?rout pt:type ?type .
					?rout pt:name ?name .
					?rout georss:line ?line .
			   }""",
			   initNs = { "rdf": RDF, "pt": PT, "georss": GEORSS },
			   initBindings={'type': Literal(type)}
			)
		
for row in res:
	print(row[0], row[1])