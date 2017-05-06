#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-26
# @Author  : Andrey Demidenko (worm2fed@mail.ru)
# @Version : 1.0

""" Module created for easy access to graph tools
"""

__version__ 	= '1.0'
__author__ 		= 'Andrey Demidenko'
__docformat__ 	= 'reStructuredText'


from glob import glob
import collections

import numpy as np
from graph_tool.all import *

from tools import *


class GraphException(Exception):
	""" Base class for errors in graph_tools module.
	""" 
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message	


class GraphTools():
	""" Directly, class contains methods for graphs
	"""
	def __init__(self):
		""" Initialisation
		"""
		self.graph 	= None
		self.ext 	= ['gt', 'graphml', 'xml', 'dot', 'gml']


	def load(self, file, ext='auto', local=True):
		""" Load graph from file

			:param file: path to file with graph
			:param ext: extention of file
			:param local: load graph localy or to return
		"""
		if glob(file):
			if ext == 'auto':
				ext = extention(file)

			if ext in self.ext:
				graph = load_graph(file)
			elif ext == 'csv':
				graph = load_graph_from_csv(file)
			else:
				raise GraphException('Error message: %s' % \
					'Unknown extention ' + str(ext))

			if local:
				self.graph = graph
			else:
				return graph
		else:
			raise GraphException('Error message: %s' % \
					'Graph ' + str(ext) + ' was not found')


	def save(self, out):
		""" Save graph to file

			:param out: path to save a graph
		"""
		if self.graph is not None:
			self.graph.save(out)
		else:
			raise GraphException('Error message: %s' % \
					'Graph is not defined')


	def build_from_vk(self, data):
		""" Build graph from VK dataset
			
			:param data: list with user ids and other info
		"""
		self.graph = Graph(directed=False)

		# Add properties (additional info about vertex)
		for k in data[0].keys():
			if k == 'friends' or k == 'city': continue
			self.graph.vp[k] = self.graph.new_vp('string')

		# Dictionary and set for indexing vertecies and edges
		id_to_vertex 	= {}
		used 			= set()
			
		# Add vertices and its data
		for u in data:
			v = self.graph.add_vertex()
			id_to_vertex[u['id']] = v

			for k in data[0].keys():
				if k == 'friends' or k == 'city': continue
				self.graph.vp[k][v] = u[k]

		# Add edges
		for u in data:
			used.add(u['id'])
			# Check is u have a friend in this data
			if 'friends' in u:
				for f in u['friends']:
					if (f['id'] not in used) and (f['id'] in id_to_vertex):
						self.graph.add_edge(id_to_vertex[u['id']], \
							id_to_vertex[f['id']])


	def delete_random_edges(self, count, percent=True):
		""" Delete random edges

			:param count: number of edges to delete
			:param percent: count in items or percents
		"""
		if self.graph is not None:
			edge_num 	= self.graph.num_edges()
			edges 		= self.graph.get_edges()
			deleted 	= []
			count 		= int(edge_num * (count / 100)) if percent else count

			for i in range(count):
				index = np.random.randint(low=0, high=(edges.shape[0] - 1))

				while index in deleted:
					index = np.random.randint(low=0, high=(edges.shape[0] - 1))

				self.graph.remove_edge(self.graph.edge(edges[index][0], \
					edges[index][1]))
				deleted.append(index)
		else:
			raise GraphException('Error message: %s' % \
					'Graph is not defined')


	def save_to_json(self, file):
		""" Convert graph to json format

			:param file: path to save json graph
		"""
		js = { 'nodes': [], 'links': [] }
		# Converting nodes
		for v in self.graph.vertices():
			info = { vp: self.graph.vp[vp][v] for vp in self.graph.vp.keys() }
			info['group'] = 1
			js['nodes'].append(info)

		# Converting edges
		for e in self.graph.edges():
			js['links'].append({ 'source': str(e.source()), \
				'target': str(e.target()), \
				'value': 1})

		save_json(js, file)

	# TODO
	def draw(self, size=(1920, 1080), out='graph.pdf', layout=''):
		""" Draw graph

			:param size: tupple with image size
			:param out: path to save an image
			:param layout: layout for graph drawing
				arf_layout(graph, max_iter=0)
		"""
		if self.graph is not None:
			with LeadTime() as t:
				# graph_draw(self.graph, pos=layout, output_size=size, output=out)
				deg = self.graph.degree_property_map('in')
				deg.a = 4 * (np.sqrt(deg.a) * 0.5 + 0.4)
				ebet = betweenness(self.graph)[1]
				ebet.a /= ebet.a.max() / 10.
				eorder = ebet.copy()
				eorder.a *= -1
				pos = sfdp_layout(self.graph)
				control = self.graph.new_edge_property('vector<double>')

				for e in self.graph.edges():
					d = np.sqrt(np.sum((pos[e.source()].a - pos[e.target()].a) ** 2))
					control[e] = [0.3, d, 0.7, d]

				graph_draw(self.graph, pos=pos, vertex_size=deg, \
					vertex_fill_color=deg, vorder=deg, edge_color=ebet, \
					eorder=eorder, edge_pen_width=ebet, edge_control_points=control, \
					output=out)
		else:
			raise GraphException('Error message: %s' % \
					'Graph ' + str(ext) + ' is not defined')


	def get_edges_list(self):
		""" Get edges list
		"""
		return self.graph.get_edges().tolist()


	def get_vertices_list(self):
		""" Get edges list
		"""
		return self.graph.get_vertices().tolist()


	def get_degrees_list(self):
		""" Get degrees list

			:return: ndarray with degrees of vertex list
		"""
		return self.graph.get_out_degrees(self.get_vertices_list())


	def get_needed_edges(self, file):
		""" Remove edges from graph in `file` which are in both local and 
		external graphs

			:param file: path to another graph
		"""
		graph = self.load(file, local=False)
		for e in self.graph.edges():
			graph.remove_edge(graph.edge(e.source(), e.target()))

		return dict(enumerate(map(set, graph.get_edges()[:,:2])))


	def get_neighbours(self):
		""" Get neighbours dict

			:return: dict with vertices as keys and neighbours list as values
		"""
		return { v: np.sort(self.graph.get_out_neighbours(v)).tolist() \
			for v in self.get_vertices_list() }


	def get_common_neighbours(self):
		""" Find common neighbours
			
			:return: dict Counter with common neighbours for each vertex
		"""
		common_neighbours 	= collections.Counter()
		neighbours 			= self.get_neighbours()
		degrees 			= self.get_degrees_list()

		# Go through all vertices
		for v in self.get_vertices_list():
			i = 1
			for n1 in neighbours[v]:
				for n2 in neighbours[v][i:]:
					common_neighbours[(n1, n2)] += 1
				i += 1

		return common_neighbours


	def get_jaccard(self):
		""" Calculate Jaccard's Coefficient
			
			:return: dict Counter with Jaccard's coefficient for each vertex
		"""
		jaccard_coef 		= collections.Counter()
		common_neighbours 	= self.get_common_neighbours()
		degrees 			= self.get_degrees_list()

		# Go through all vertices
		for common_key in common_neighbours.elements():
			jaccard_coef[common_key] = common_neighbours[common_key] / \
				(degrees[common_key[0]] + degrees[common_key[1]] - \
					common_neighbours[common_key])

		return jaccard_coef


	def get_adamic_adar(self):
		""" Calculate Adamic/Adar Coefficient
			
			:return: dict Counter with Adamic/Adar coefficient for each vertex
		"""
		adamic_adar 	= collections.Counter()
		neighbours 		= self.get_neighbours()
		degrees 		= self.get_degrees_list()

		# Go through all vertices
		for v in self.get_vertices_list():
			i = 1
			for n1 in neighbours[v]:
				for n2 in neighbours[v][i:]:
					adamic_adar[(n1, n2)] += 1 / np.log(degrees[v])
				i += 1

		return adamic_adar