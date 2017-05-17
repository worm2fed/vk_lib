#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-07
# @Author  : Andrey Demidenko (worm2fed@mail.ru)
# @Version : 1.0

""" 

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
	""" Class for parsing HTML pages, in our case - vk.com/catalog.php
    """
    def __init__(self, site, *args, **kwargs):
		""" Initialisation
			
			:param site: site name
			:param *args:
			:param **kwargs:
    	"""
		self.links 	= []
		self.site 	= site
		# Call parent's __init__
		super().__init__(*args, **kwargs)
		# Due initialisation 'feed' page content to parser
		self.feed(self.read_site_content())
		# Save links to file
		self.write_to_file()


    def _get_request_url(self, method_name, parameters):
		""" Generate request URL

			:param method_name: name of method in VK API
			:param parameters: string with parameters for request
    	"""
		return ('https://api.vk.com/method/{method_name}?{parameters}'\
			'&v={api_v}').format(
			method_name=method_name, api_v=self.api_v, parameters=parameters)