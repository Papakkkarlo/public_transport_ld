import rdflib
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF
import json

#onto_path = "owl/public_transport.owl"
#public_transport = Graph().parse(onto_path, format=rdflib.util.guess_format(onto_path))

PT = Namespace("http://www.semanticweb.org/user/ontologies/2019/4/untitled-ontology-42#")
GEORSS = Namespace("http://www.georss.org/georss/")

json_file = open('data/stops.geojson')  
stops = json.load(json_file)['features']
json_file.close()

bus_stops_added = []
buses_added = []

g = Graph()
for s in stops:
	try:
		name = s['properties']['name'].replace(' ','_').replace('"','')
	except:
		print(s)
	bus_stop = PT[name]
	stop = PT[name + '/' + s['properties']['rout'].replace('/','')]
	bus = PT[s['properties']['rout'].replace('/','')]
	
	if bus not in buses_added:
		g.add( (bus, RDF.type, PT.bus) )
		g.add( (bus, PT.name, Literal(s['properties']['rout'].replace('/',''))) )
		buses_added.append(bus)

	if bus_stop not in bus_stops_added:	
		g.add( (bus_stop, RDF.type, PT.bus_stop) )
		g.add( (bus_stop, PT.type, Literal(s['properties']['type'])) )
		g.add( (bus_stop, PT.name, Literal(s['properties']['name'])) )
		g.add( (bus_stop, GEORSS.point, Literal('-'.join([str(n) for n in s['geometry']['coordinates']]))) )
		bus_stops_added.append(bus_stop)

	g.add( (stop, RDF.type, PT.stop) )
	g.add( (stop, PT.onBusStop, bus_stop) )
	g.add( (stop, PT.ofBus, bus) )
	g.add( (stop, PT.onRout, PT[s['properties']['rout']]) )

json_file = open('data/public_transport_routs.geojson')  
routs = json.load(json_file)['features']
json_file.close()

for r in routs[:100]:
	rout = PT[r['properties']['href']]
	g.add( (rout, RDF.type, PT.rout) )
	g.add( (rout, PT.direction, Literal(r['properties']['direction'])) )
	g.add( (rout, PT.type, Literal(r['properties']['type'])) )
	g.add( (rout, PT.number, Literal(r['properties']['number'])) )
	g.add( (rout, PT.name, Literal(r['properties']['href'])) )
	g.add( (rout, GEORSS.line, Literal(' '.join(['-'.join([str(n) for n in l]) for l in r['geometry']['coordinates']]))) )

type = 'trolleybus'
res = g.query(
			"""SELECT ?name ?line
			   WHERE {
					?rout pt:type  ?type.
					?rout pt:name ?name .
					?rout georss:line ?line .
			   }""",
			   initNs = { "rdf": RDF, "pt": PT, "georss": GEORSS },
			   initBindings={'rout': PT[type]}
			)
		
for row in res:
	print(row[0], row[1])
#g.serialize('data/public_transport_KB', format='turtle')