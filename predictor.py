#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-05
# @Author  : Andrey Demidenko (worm2fed@mail.ru)
# @Version : 1.0

""" Module for Link Prediction
"""

__version__ 	= '1.0'
__author__ 		= 'Andrey Demidenko'
__docformat__ 	= 'reStructuredText'


class PredictorException(Exception):
	""" Base class for errors in predictor module.
	""" 
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message	


class Predictor():
	""" Class for prediction
	"""
	def __init__(self):
		""" Initialisation
		"""
		pass


	def topology_predictor(self, coef, threshold, check_edges=None):
		""" Predictor
			
			:param coef: coefficient like common neighbours, Adamic/Adar, 
		Jaccaard, etc.
			:param threshold: predictor threshold
			:param check_edges: dict with edges to check prediction

			:return: if `check_edges` is empty returns dict with edges, 
		otherwise dict with hits
		"""
		if check_edges is not None:
			if isinstance(check_edges, dict):
				return dict(enumerate(e for e in check_edges.values() \
					if e in predicted_edges.values()))
			else:
				raise PredictorException('Error message: %s' % \
					'check_edges should be <class \'dict\'>')
		else:
			return dict(enumerate(map(lambda x: set(x[0]), \
				coef.most_common(threshold))))