#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-26
# @Author  : Andrey Demidenko (worm2fed@mail.ru)
# @Version : 1.0

""" This module allows to use VK API more comfortable.
"""

__version__ 	= '1.0'
__author__ 		= 'Andrey Demidenko'
__docformat__ 	= 'reStructuredText'

title = 'Module for VK API access'


import getopt
import requests

from tools import *


class VkException(Exception):
	""" Base class for errors in vk_api module.
	""" 
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message		


class VkApi():
	""" Directly, class contains methods for VK API
	"""
	def __init__(self, api_v, token):
		""" Initialisation

			:param api_v: VK API version
			:param token: access token
    	"""
		self.api_v = api_v
		self.token = token
		

	def _get_request_url(self, method_name, parameters, access_token=False):
		""" Generate request URL

			:param method_name: name of method in VK API
			:param parameters: string with parameters for request
			:param access_token: is access token needed
    	"""
		request_url = ('https://api.vk.com/method/{method_name}?{parameters}'\
			'&v={api_v}').format(
			method_name=method_name, api_v=self.api_v, parameters=parameters)

		# Add access token if needed
		if access_token:
			request_url = '{}&access_token={token}'.format(request_url, \
				token=self.token)

		return request_url


	def get_user_info(self, uid, fields=''):
		""" Returns user/users profile info with `fields`

			:param uid: user id
			:param fields: fields wich are needed to get
		"""
		print('Collecting info about user ' + str(uid) + '...')
		result = requests.get(self._get_request_url('users.get', \
			'user_ids=%s&fields=%s' % (uid, fields))).json()

		if 'error' in result.keys():
			raise VkException('Error message: %s Error code: %s' % \
				(result['error']['error_msg'], result['error']['error_code']))
		
		return result['response']


	def get_friends_list(self, uid, city=''):
		""" Returns user's friend list

			:param uid: user id to get friends list
			:param city: city id to filter results
		"""
		result = list()
		print('Collecting friends list of user ' + str(uid) + '...')
		tmp = requests.get(self._get_request_url('friends.get', \
			'user_id=%s&fields=city,photo' % uid)).json()

		if 'error' in tmp.keys():
			raise VkException('Error message: %s Error code: %s' % \
				(tmp['error']['error_msg'], tmp['error']['error_code']))

		tmp = tmp['response']['items']
		# Check is user exactly in city
		if city:
			for i in tmp:
				if 'city' in i:
					if i['city']['id'] == city:
						result.append(i)
		else:
			result += tmp

		print('Found ' + str(len(result)) + ' friends of user ' + str(uid))

		return result


	def get_followers_list(self, uid, city=''):
		""" Returns user's followers list

			:param uid: user id to get followers list
			:param city: city id to filter results
		"""
		result = list()
		offset = 0
		current = 0

		print('Collecting followers list of user ' + str(uid) + '...')
		while True:
			tmp = requests.get(self._get_request_url('users.getFollowers', \
				'user_id=%s&fields=city,photo&count=%s&offset=%s' % (uid, \
					1000, offset), access_token=True))\
			.json()

			if 'error' in tmp.keys():
				raise VkException('Error message: %s Error code: %s' % \
					(tmp['error']['error_msg'], tmp['error']['error_code']))

			tmp = tmp['response']['items']
			offset += 1000
			if len(tmp) == 0:
				break

			# Check is user exactly in city
			if city:
				for i in tmp:
					if 'city' in i:
						if i['city']['id'] == city:
							result.append(i)
							current += 1
			else:
				result += tmp
				current += len(tmp)

		print('Found ' + str(len(result)) + ' followers of user ' + str(uid))

		return result


	def get_users_from_group(self, group, count, city=''):
		""" Returns a `count` of users from `group` and `city`

			:param group: group id to search in
			:param count: nuber of users to get
			:param city: city id to filter results
		"""
		result = list()
		offset = 0
		current = 0

		print('Collecting users from group ' + str(group) + '...')
		while current in range(count):
			get_count = lambda: count if 1000 - count >= 0 else \
						count - current if count - current <= 1000 else \
						1000
			tmp = requests.get(self._get_request_url('groups.getMembers', \
				'group_id=%s&fields=city,photo&count=%s&offset=%s' % (group, \
					get_count(), offset), access_token=True))\
			.json()

			if 'error' in tmp.keys():
				raise VkException('Error message: %s Error code: %s' % \
					(tmp['error']['error_msg'], tmp['error']['error_code']))

			tmp = tmp['response']['items']
			offset += get_count()
			if len(tmp) == 0:
				break

			# Check is user exactly in city
			if city:
				for i in tmp:
					if current >= count:
						break
				
					if 'city' in i:
						if i['city']['id'] == city:
							result.append(i)
							current += 1
			else:
				result += tmp
				current += len(tmp)

		return result


	def get_countries(self, code=''):
		""" Returns a countries list

			:param code: two-letters country code ISO 3166-1
		"""
		print('Collecting countries...')
		result = requests.get(self._get_request_url('database.getCountries', \
			'need_all=1&code=%s' % code)).json()

		return result['response']['items']


	def get_regions(self, country):
		""" Returns a country's regions list

			:param country: country id to get regions
		"""
		print('Collecting regions of count ' + str(country) + '...')
		result = requests.get(self._get_request_url('database.getRegions', \
			'country_id=%s' % country)).json()

		return result['response']['items']


	def get_cities(self, country, region='', count=1000, get_all=False):
		""" Returns a country's cities list

			:param country: country id
			:param region: region id
			:param count: number of cities to get
			:param get_all: te get all cities list
		"""
		result = list()
		offset = 0
		current = 0

		print('Collecting cities from country ' + str(country) + '...')
		while current in range(count):
			get_count = lambda: count if 1000 - count >= 0 else \
						count - current if count - current <= 1000 else \
						1000
			tmp = requests.get(self._get_request_url('database.getCities', \
				'need_all=1&country_id=%s&region_id=%s&count=%s&offset=%s' % \
				(country, region, get_count(), offset)))\
			.json()['response']['items']
			offset += get_count()

			if len(tmp) == 0:
				break
			
			result += tmp

			if not get_all:
				current += len(tmp)

		return resul


def help():
	""" Print help
	"""
	print(title + '\n')
	print('Usage:')
	print('\t-v, --verbose\t\tEnable verbose mode')
	print('\t-h, --help\t\tShow this help and exit')
	print('\t-V, --version\t\tShow version info and exit')


if __name__ == '__main__':
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
			print('vk_api module v' + __version__)
			quit()
		elif opt in ('-v', '--verbose'):
			verbose(True)
	else:
		help()
		quit()