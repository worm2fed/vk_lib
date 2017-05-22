#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-07
# @Author  : Andrey Demidenko (worm2fed@mail.ru)
# @Version : 1.0

""" Module implements parsing tools

""" 

__version__ 	= '1.0'
__author__ 		= 'Andrey Demidenko'
__docformat__ 	= 'reStructuredText'

import re

from html.parser import HTMLParser
from urllib.request import urlopen

from tools import *


class ParserException(Exception):
	""" Base class for errors in parser module
	""" 
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message		


class Parser(HTMLParser):
	""" Class for parsing HTML pages
    """
	def __init__(self, site, tags=[]):
		""" Initialisation
			
			:param site: site name
			:param tags: list with dicts to search (tag, attr, pattern)
    	"""
		self.tags 		= tags
		self.site 		= site
		self.result 	= dict()
		
		# Create a result dict with tag as key and list with value
		for tag in self.tags:
			self.result[tag['tag']] = []

		# Call parent's __init__
		super().__init__()
		# Due initialisation 'feed' page content to parser
		self.feed(self.read_site_content())


	def handle_starttag(self, current_tag, attrs):
		""" Some action when we meet hatml tag

			:param tag: html tag
			:param attrs: tag attributes
		"""
		for tag in self.tags:
			# if we found a link	
			if tag['tag'] == current_tag:
				# find tag attribute
				for attr in attrs:
					if tag['attr'] == attr[0]:
						# check is in result and validate with pattern
						pattern = re.compile(tag['pattern'])
						if pattern.match(attr[1]) and \
								attr[1] not in self.result[current_tag]:
							# save to result
							self.result[current_tag].append(attr[1])


	def read_site_content(self):
		""" Method to open page and call it's content
		"""
		return str(urlopen(self.site).read())