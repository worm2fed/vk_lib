#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-26
# @Author  : Andrey Demidenko (worm2fed@mail.ru)
# @Version : 1.0

""" Module created for easy access to graph tools
"""

__version__ = '1.0'
__author__ = 'Andrey Demidenko'
__docformat__ = 'reStructuredText'


title = 'Module for working with graphs'


import getopt
from glob import glob

from numpy import *
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

    		:param v: verbose mode
		"""
		self.graph = None
		self.ext = ['gt', 'graphml', 'xml', 'dot', 'gml']


	def load(self, file, ext='auto'):
		""" Load graph from file

			:param file: path to file with graph
			:param ext: extention of file
		"""
		print('Loading graph ' + str(file) + '...')
		if glob(file):
			if ext == 'auto':
				ext = extention(file)

			if ext in self.ext:
				self.graph = load_graph(file)
			elif ext == 'csv':
				self.graph = load_graph_from_csv(file)
			else:
				raise GraphException('Error message: %s' % \
					'Unknown extention ' + str(ext))
			
			print('Vertices: ' + str(self.graph.num_vertices()) + \
					' Edges: ' + str(self.graph.num_edges()))
		else:
			raise GraphException('Error message: %s' % \
					'Graph ' + str(ext) + ' was not found')


	def save(self, out):
		""" Save graph to file

			:param out: path to save a graph
		"""
		print('Saving to file...')
		if self.graph is not None:
			self.graph.save(out)
		else:
			raise GraphException('Error message: %s' % \
					'Graph is not defined')


	def build_from_vk(self, data):
		""" Build graph from VK dataset
			
			:param data: list with user ids and other info
		"""
		print('Building graph...')
		self.graph = Graph(directed=False)

		for k in data[0].keys():
			print('Found property ' + str(k))
			if k == 'friends' or k == 'city': 
				print('Skipping')
				continue
			self.graph.vp[k] = self.graph.new_vp('string')

		# Dictionaries for indexing vertecies and edges
		id_to_vertex = dict()
		used = set()
			
		# Add vertices and its data
		print('Adding vertices and its data to graph...')
		for u in data:
			v = self.graph.add_vertex()
			id_to_vertex[u['id']] = v

			for k in data[0].keys():
				for k in data[0].keys():
					if k == 'friends' or k == 'city': continue
					self.graph.vp[k][v] = u[k]

		# Add edges
		print('Adding edges to graph...')
		for u in data:
			used.add(u['id'])
			# Check is u have a friend in this data
			for f in u['friends']:
				if (f['id'] not in used) and (f['id'] in id_to_vertex):
					self.graph.add_edge(id_to_vertex[u['id']], id_to_vertex[f['id']])

		print('Vertices: ' + str(self.graph.num_vertices()) + \
					' Edges: ' + str(self.graph.num_edges()))


	def delete_random_edges(self, count, percent=True):
		""" Delete random edges

			:param count: number of edges to delete
			:param percent: count in items or percents
		"""
		print('Deleting ' + (str(count) + '%' if percent else str(count)) + \
			' edges')
		if self.graph is not None:
			edge_num = self.graph.num_edges()
			edges = self.graph.get_edges()
			deleted = []
			count = int(edge_num * (count / 100)) if percent else count

			for i in range(count):
				index = random.randint(low=0, high=(edges.shape[0] - 1))

				while index in deleted:
					index = random.randint(low=0, high=(edges.shape[0] - 1))

				self.graph.remove_edge(self.graph.edge(edges[index][0], \
					edges[index][1]))
				deleted.append(index)
			else:
				print(str(len(deleted)) + ' edges was successfuly deleted')
		else:
			raise GraphException('Error message: %s' % \
					'Graph is not defined')


	def save_to_json(self, file):
		""" Convert graph to json format

			:param file: path to save json graph
		"""
		js = { 'nodes': [], 'links': [] }
		# Converting nodes
		print('Converting vertices and its data...')
		for v in self.graph.vertices():
			info = dict()

			for vp in self.graph.vp.keys():
				info[vp] = self.graph.vp[vp][v]

			info['group'] = 1
			js['nodes'].append(info)

		# Converting edges
		print('Converting edges...')
		for e in self.graph.edges():
			js['links'].append({ 'source': str(e.source()), \
				'target': str(e.target()), \
				'value': 1})

		save_json(js, file)


	def draw(self, size=(1920, 1080), file='graph.png', layout=''):
		""" Draw graph

			:param size: tupple with image size
			:param file: path to save an image
			:param layout: layout for graph drawing
			arf_layout(graph, max_iter=0)
		"""
		with LeadTime() as t:
			deg = self.graph.degree_property_map('in')
			deg.a = 4 * (sqrt(deg.a) * 0.5 + 0.4)
			ebet = betweenness(self.graph)[1]
			ebet.a /= ebet.a.max() / 10.
			eorder = ebet.copy()
			eorder.a *= -1
			pos = sfdp_layout(self.graph)
			control = self.graph.new_edge_property('vector<double>')

			for e in self.graph.edges():
				d = sqrt(sum((pos[e.source()].a - pos[e.target()].a) ** 2))
				control[e] = [0.3, d, 0.7, d]

			graph_draw(self.graph, pos=pos, vertex_size=deg, \
				vertex_fill_color=deg, vorder=deg, edge_color=ebet, \
				eorder=eorder, edge_pen_width=ebet, edge_control_points=control, \
				output='graph.pdf')
		# print('Drawing graph...')
		# if self.graph is not None:
		# 	with LeadTime() as t:
		# 		graph_draw(self.graph, pos=layout, output_size=size, output=file)
		# else:
		# 	raise GraphException('Error message: %s' % \
		# 			'Graph ' + str(ext) + ' is not defined')