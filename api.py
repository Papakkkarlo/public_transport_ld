import rdflib
from rdflib import Graph, Namespace
from rdflib.namespace import RDF

import sys
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

#parser = reqparse.RequestParser()
#parser.add_argument('rout')
#parser.add_argument('buss_stop')

KB_path = "data/public_transport_KB"
g = Graph()
g.parse(KB_path, format="turtle")
PT = Namespace("http://www.semanticweb.org/user/ontologies/2019/4/untitled-ontology-42#")
GEORSS = Namespace("http://www.georss.org/georss")

class Routs(Resource):
	def get(self):
		buss_stop = 'Уральская_улица'
		res = g.query(
			"""SELECT ?name ?line
			   WHERE {
					?rout rdf:type pt:rout .
					?rout pt:name ?name .
					?rout georss:line ?line .
			   }""",
			   initNs = { "rdf": RDF, "pt": PT, "georss": GEORSS},
			   initBindings={'buss_stop': PT[buss_stop]}
			)
		response = []
		for row in res:
			response.append({'name': row[0], 'coordinates': row[1]})
		return response



class Buss_stops(Resource):
	def get(self, type, numb):
		rout = '/%s/%s' % (type, numb)
		res = g.query(
			"""SELECT ?name ?type ?point
			   WHERE {
					?buss_stop pt:onRout ?rout .
					?buss_stop pt:name ?name .
					?buss_stop pt:type ?type .
					?buss_stop georss:point ?point .
			   }""",
			   initNs = { "rdf": RDF, "pt": PT, "georss": GEORSS },
			   initBindings={'rout': PT[rout]}
			)
		response = []
		for row in res:
			response.append({'name': row[0], 'type': row[1], 'coordinates': row[2]})
		return response
 

class Busses(Resource):
	def get(self, buss_stop):
		buss_stop = 'Уральская_улица'
		res = g.query(
			"""SELECT ?name
			   WHERE {
					?stop pt:onBussStop ?buss_stop .
					?stop pt:ofBuss ?buss .
					?buss pt:name ?name
			   }""",
			   initNs = { "rdf": RDF, "pt": PT },
			   initBindings={'buss_stop': PT[buss_stop]}
			)
		response = []
		for row in res:
			response.append({'buss': row})
		return response

api.add_resource(Routs, '/')
api.add_resource(Buss_stops, '/stops/<type>/<numb>')
api.add_resource(Busses, '/busses/<buss_stop>')

if __name__ == '__main__':
	app.run(debug=True)