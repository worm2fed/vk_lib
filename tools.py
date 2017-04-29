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


import time
import sys
import os


class LeadTime(object):
	""" Class to elapse time
	"""
	def __enter__(self):
		self._startTime = time.time()
        

	def __exit__(self, type, value, traceback):
		print('Elapsed time: {:.3f} sec '.format(time.time() - self._startTime))


# Method to clean up a console
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
# Method to quit
quit = lambda mes='': sys.exit(mes)
# Method to go back and stop function
back = lambda: False
stop = lambda: True
# Get file extension
extension = lambda f: os.path.splitext(f)