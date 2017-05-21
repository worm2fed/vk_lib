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
	def __init__(self, site):
		""" Initialisation
			
			:param site: site name
			:param *args:
			:param **kwargs:
    	"""
		self.links 	= []
		self.site 	= site
		# Call parent's __init__
		super().__init__()
		# Due initialisation 'feed' page content to parser
		self.feed(self.read_site_content())


	def is_valid(self, link, pattern=''):
		""" Method to link validation

			**Note**
			We should add link if:
			1) Link is not in `links`
			2) If this link isn't JS call
			3) If it's not a label (don't have '#')

			:param link: link for validation
		"""
		return link not in self.links or '#' not in link or 'javascript:' not in link


	def handle_starttag(self, tag, attrs, pattern=''):
		""" Some action when we meet hatml tag

			:param tag: html tag
			:param attrs: tag attributes
		"""
		# if we fount a link
		if tag == 'a':
			# find link attribute
			for attr in attrs:
				if attr[0] == 'href':
					# check this link with validate() method
					if self.is_valid(attr[0], pattern):
						# save to links
						self.links.append(attr[1])


	def read_site_content(self):
		""" Method to open page and call it's content
		"""
		return str(urlopen(self.site).read())