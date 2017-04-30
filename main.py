#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-26
# @Author  : Andrey Demidenko (worm2fed@mail.ru)
# @Version : 1.0

""" This is conditional point of entry to entire project
"""

__version__ = '1.0'
__author__ = 'Andrey Demidenko'
__docformat__ = 'reStructuredText'


import getopt

from settings import *
from menu_options import *
from tools import *
from vk_api import *
from graph_tools import *


_verbose = False
_vk_api = VkApi(api_v, token)


def menu(section, options):
	""" Print action menu
	"""
	global _verbose
	clear()
	print('\n* ' + section + ' *')
	print('_' * len(section) + '_' * 4 + '\n')

	for op in options:
		print('\t' + str(op['index']) + '. \t' + str(op['title']))
	print('\n\tVerbose mode: ' + ('on' if _verbose else 'off') + \
		' (enter v to switch)')
	
	option = input('\nSelect option: ')
	if option == 'v':
		_verbose = not _verbose
		return True
	elif int(option) not in range(1, len(options) + 1):
		return True
	else:
		method = globals().get(options[int(option) - 1]['method'])
		if not method:
			raise NotImplementedError('Method %s() not implemented' % \
				options[int(option) - 1]['method'])

		return method(**options[int(option) - 1]['args'])


def help():
	""" Print help
	"""
	print(title + '\n')
	print('Usage:')
	print('\t-v, --verbose\t\tEnable verbose mode')
	print('\t-h, --help\t\tShow this help and exit')
	print('\t-V, --version\t\tShow version info and exit')


def main():
	""" Launch project with command line arguments
	"""
	global _verbose

	try:
		opts, args = getopt.getopt(sys.argv[1:], 'hvV', \
			['help', 'verbose', 'version'])
	except getopt.GetoptError as err:
		quit((str(err) + '\n\nTry -h or --help for help'))
	
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			help()
			quit()		
		elif opt in ('-V', '--version'):
			print('vk_lib v' + __version__)
			quit()
		elif opt in ('-v', '--verbose'):
			_verbose = True
	else:
		while menu(title, main_options):
			pass
		else:
			quit()


if __name__ == '__main__':
	main()