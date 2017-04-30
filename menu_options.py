#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-26
# @Author  : Andrey Demidenko (worm2fed@mail.ru)
# @Version : 1.0

""" This is file with menu options for `main.py`
"""

title = 'VK Network parsing and Link Prediction utility'

vk_api_options = [
	{ 'index': 1, 'title': 'Get user info', 
		'method': '', 'args': { 

		} 
	},
	{ 'index': 2, 'title': 'Get friends list', 
		'method': '', 'args': { 

		} 
	},
	{ 'index': 3, 'title': 'Get users from group', 
		'method': '', 'args': { 

		} 
	},
	{ 'index': 4, 'title': 'Get countries', 
		'method': '', 'args': { 

		} 
	},
	{ 'index': 5, 'title': 'Get regions', 
		'method': '', 'args': { 

		} 
	},
	{ 'index': 6, 'title': 'Get cities', 
		'method': '', 'args': { 

		} 
	},
	{ 'index': 7, 'title': '<< Back', 
		'method': 'stop', 'args': {  
		} 
	},
]
graph_tool_options = [
	{ 'index': 1, 'title': 'Build', 
		'method': 'menu', 'args': { 

		} 
	},
	{ 'index': 2, 'title': 'Load', 
		'method': 'menu', 'args': { 

		} 
	},
	{ 'index': 3, 'title': 'Save', 
		'method': 'menu', 'args': { 

		} 
	},
	{ 'index': 4, 'title': 'Draw', 
		'method': 'menu', 'args': { 

		} 
	},
	{ 'index': 5, 'title': '2WEB', 
		'method': 'menu', 'args': { 

		} 
	},
	{ 'index': 6, 'title': 'Delete random edges', 
		'method': 'menu', 'args': { 

		} 
	},
	{ 'index': 7, 'title': '<< Back', 
		'method': 'stop', 'args': {  
		} 
	},
]
topology_predictor_options = [
	{ 'index': 1, 'title': 'Common Neighboors', 
		'method': '', 'args': { 

		} 
	},
	{ 'index': 2, 'title': 'Jaccard\'s Coefficient', 
		'method': '', 'args': { 

		} 
	},
	{ 'index': 3, 'title': 'Adamic/Adar Coefficient', 
		'method': '', 'args': { 

		} 
	},
	{ 'index': 4, 'title': '<< Back', 
		'method': 'stop', 'args': {  
		} 
	},
]
vk_catalog_parser_options = [
	{ 'index': 1, 'title': '<< Back', 
		'method': 'stop', 'args': {  
		} 
	},
]
main_options = [
	{ 'index': 1, 'title': 'VK API', 
		'method': 'menu', 'args': { 
			'section': 'VK API', 
			'options': vk_api_options 
		} 
	},
	{ 'index': 2, 'title': 'Graph Tools', 
		'method': 'menu', 'args': { 
			'section': 'Graph Tools', 
			'options': graph_tool_options 
		} 
	},
	{ 'index': 3, 'title': 'Topology Predictor', 
		'method': 'menu', 'args': { 
			'section': 'Topology Predictor', 
			'options': topology_predictor_options 
		} 
	},
	{ 'index': 4, 'title': 'VK Catalog Parser', 
		'method': 'menu', 'args': { 
			'section': 'VK Catalog Parser', 
			'options': vk_catalog_parser_options 
		} 
	},
	{ 'index': 5, 'title': 'Quit', 
		'method': 'quit', 'args': {
		} 
	},
]
