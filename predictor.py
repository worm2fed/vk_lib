from graph_tool.all import *
from glob import glob
import numpy as np
import collections

class Predictor():
	# Initialisation
	def __init__(self, filename, v=True):
		if v:
			print('Loading graph...')
		# Load graph
		if glob(filename):
			self.graph = load_graph(filename)
			if v:
				print('Vertices: ' + str(self.graph.num_vertices()) + ' Edges: ' + str(self.graph.num_edges()))
		# Else exit
		else:
			print('Graph was not found! Exiting')
			sys.exit(0)

	# Get score, i.e. find common neighbours
	def get_common_neighbours(self, neighbours, vertices):
		common_neighbours = collections.Counter()

		# Go through all vertices
		for v in vertices.tolist():
			i = 1
			for n1 in neighbours[v]:
				for n2 in neighbours[v][i:]:
					common_neighbours[(n1, n2)] += 1
				i += 1

		return common_neighbours

	# Calculate Jaccard's Coefficient
	def get_jaccard_coef(self, degrees, common_neighbours):
		jaccard_coef = collections.Counter()

		# Go through all vertices
		for common_key in common_neighbours.elements():
			jaccard_coef[common_key] = common_neighbours[common_key] / (degrees[common_key[0]] + degrees[common_key[1]] - common_neighbours[common_key])

		return jaccard_coef

	# Calculate Adamic/Adar Coefficient
	def get_adamic_adar(self, neighbours, vertices, degrees):
		adamic_adar = collections.Counter()

		# Go through all vertices
		for v in vertices.tolist():
			i = 1
			for n1 in neighbours[v]:
				for n2 in neighbours[v][i:]:
					adamic_adar[(n1, n2)] += 1 / np.log(degrees[v])
				i += 1

		return adamic_adar

	# Predictor
	def predictor(self, left_edges, coef, missing):
		predicted_edges = dict(enumerate(map(lambda x: set(x[0]), coef.most_common(missing))))
		hits = 0

		for le in left_edges.values():
			if le in predicted_edges.values():
				hits += 1

		return hits

# Start
if __name__ == '__main__':
	a = Predictor('new_graph.xml')
	b = Predictor('graph.xml', False)

	# Delete from graph all edges wich are in a.graph
	for e in a.graph.edges():
		b.graph.remove_edge(b.graph.edge(e.source(), e.target()))
	left_edges = dict(enumerate(map(set, b.graph.get_edges()[:,:2])))

	missing = int(a.graph.num_edges() * 10 / 8 - a.graph.num_edges())
	vertices = a.graph.get_vertices()
	neighbours = {v:np.sort(a.graph.get_out_neighbours(v)).tolist() for v in vertices.tolist()}
	degrees = a.graph.get_out_degrees(vertices)

	common_neighbours = a.get_common_neighbours(neighbours, vertices)
	jaccard_coef = a.get_jaccard_coef(degrees, common_neighbours)
	adamic_adar_coef = a.get_adamic_adar(neighbours, vertices, degrees)

	cn = a.predictor(left_edges, common_neighbours, missing)
	print('\nAccuracy with Common Neighbours predictor is ' + str(cn * 100 / missing) + '%, ' + str(cn) + ' edges were successfuly predicted')

	jaccard = a.predictor(left_edges, jaccard_coef, missing)
	print('Accuracy with Jaccard\'s Coefficient predictor is ' + str(jaccard * 100 / missing) + '%, ' + str(jaccard) + ' edges were successfuly predicted')

	adamic_adar = a.predictor(left_edges, adamic_adar_coef, missing)
	print('Accuracy with Adamic/Adar predictor is ' + str(adamic_adar * 100 / missing) + '%, ' + str(adamic_adar) + ' edges were successfuly predicted')

	print('Saving to file...')
	with open('results', 'a') as file:
		file.write(str(cn * 100 / missing) + ',' + str(jaccard * 100 / missing) + ',' + str(adamic_adar * 100 / missing) + '\n')