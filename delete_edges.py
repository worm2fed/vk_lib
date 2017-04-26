from graph_tool.all import *
import numpy as np
from glob import glob

class DE():
	# Initialisation
	def __init__(self):
		print('Loading graph...')
		# Load graph
		if glob('graph.xml'):
			self.graph = load_graph('graph.xml')
			print('Vertices: ' + str(self.graph.num_vertices()) + ' Edges: ' + str(self.graph.num_edges()))
		# Else exit
		else:
			print('Graph was not found! Exiting')
			sys.exit(0)

	# Delete 20% of edges
	def delete_edges(self, graph, percent):
		print('Deleting ' + str(percent) + '% of edges')
		edge_num = graph.num_edges()
		edges = graph.get_edges()
		deleted = []

		for i in range(int(edge_num * (percent / 100))):
			index = np.random.randint(low=0, high=(edges.shape[0] - 1))

			while index in deleted:
				index = np.random.randint(low=0, high=(edges.shape[0] - 1))

			graph.remove_edge(graph.edge(edges[index][0], edges[index][1]))
			deleted.append(index)
		else:
			print(str(i) + ' edges was successfuly deleted')

		return graph

# Start
if __name__ == '__main__':
	a = DE()
	new_graph = a.delete_edges(a.graph, 20)

	print('Saving to file...')
	new_graph.save('new_graph.xml')