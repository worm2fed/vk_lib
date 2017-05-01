#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-26
# @Author  : Andrey Demidenko (worm2fed@mail.ru)
# @Version : 1.0

""" This is set of different tools
"""

__version__ = '1.0'
__author__ = 'Andrey Demidenko'
__docformat__ = 'reStructuredText'


from glob import glob
import pickle
import time
import json
import sys
import os


class ToolsException(Exception):
	""" Base class for errors in tools module.
	""" 
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message	


class LeadTime(object):
	""" Class to elapse time
	"""
	def __enter__(self):
		self._startTime = time.time()
        

	def __exit__(self, type, value, traceback):
		print('Elapsed time: {:.3f} sec '.format(time.time() - self._startTime))


# Get file extension
extention = lambda f: os.path.splitext(f)[1][1:]
# Get ids
get_ids = lambda lst: [u['id'] for u in lst]
# Split list to parts by 25 elements
make_parts = lambda lst, n=25: (lst[i:i + n] for i in iter(range(0, len(lst), n)))
# Make targets for vk_api
make_targets = lambda lst: ','.join(str(id) for id in lst)


def save_json(data, out):
	""" Save json to file

		:param data: data to save
		:param out: path to save a data
	"""
	print('Saving json to file...')
	with open(out, 'w') as f:
		f.write(json.JSONEncoder().encode(data))


def save_data(data, out):
	""" Save data to file

		:param data: data to save
		:param out: path to save a data
	"""
	print('Saving data to file...')
	with open(out, 'wb') as f:
		pickle.dump(data, f)


def load_data(file):
	""" Save data to file

		:param out: path to load a data
	"""
	print('Loading data from file...')
	if glob(file):
		with open(file, 'rb') as f:
			return pickle.load(f)
	else:
		raise ToolsException('Error message: %s' % \
					'File ' + str(file) + ' was not found')