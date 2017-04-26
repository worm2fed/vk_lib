import json
import sys

from graph_tool.all import *
from glob import glob
from settings import *
from main import *

class D3():
	# Initialisation
	def __init__(self):
		# Create object with tools
		self.vk_tools = VkTools(api_v, token, count, city, fields, group)
		print('Loading graph...')
		# Load graph
		if glob('graph.xml'):
			self.graph = load_graph('graph.xml')
			print('Done!')
			print('Vertices: ' + str(self.graph.num_vertices()) + ' Edges: ' + str(self.graph.num_edges()))
		# Else exit
		else:
			print('Graph was not found! Exiting')
			sys.exit(0)

		# Create json file
		self.js = {"nodes": [], "links": []}
		with Profiler() as p:
			self.write_json(self.to_json())


	# Convert graph to json format
	def to_json(self):
		# Create nodes
		for v in self.graph.vertices():
			print('Vertex:' + str(v))
			# Get user info
			info = self.vk_tools.get_user_info(self.graph.vertex_properties['id'][v])

			self.js['nodes'].append({"name": "%s %s" % (info['first_name'], info['last_name']), 
									"group": 1, 
									"photo": info['photo']})


		# Create links
		for e in self.graph.edges():
			print('Edge:' + str(e))
			# print('source: ' + str(e.source().) + ', target: ' + str(e.target()))
			self.js['links'].append({"source": str(e.source()),
									"target": str(e.target()), 
									"value": 1})

		return json.JSONEncoder().encode(self.js)

	# Save json file
	def write_json(self, json):
		with open("web/graph.json","w") as file:
			file.write(json)

# Start
if __name__ == '__main__':
	a = D3()