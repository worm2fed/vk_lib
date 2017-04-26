#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-26
# @Author  : Andrey Demidenko (worm2fed@mail.ru)
# @Version : 1.0

""" This module allows to use VK API more comfortable.
"""

__version__ = '1.0'
__author__ = 'Andrey Demidenko'
__docformat__ = 'reStructuredText'


import requests


class VkException(Exception):
	""" Base class for errors in vk_api package.
	""" 
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message		


class VkApi():
	""" Directly, class contains methods for VK API
	"""
	def __init__(self, *pargs):
		""" Initialisation
    	"""
		self.api_v, self.token = pargs
		

	def _get_request_url(self, method_name, parameters, access_token=False):
		""" Generate request URL
    	"""
		request_url = ('https://api.vk.com/method/{method_name}?{parameters}'
			'&v={api_v}').format(
			method_name=method_name, api_v=self.api_v, parameters=parameters)

		# Add access token if needed
		if access_token:
			request_url = '{}&access_token={token}'.format(request_url, \
				token=self.token)

		return request_url


	def get_user_info(self, uid, fields=''):
		""" Returns user/users profile info with `fields`
		"""
		result = requests.get(self._get_request_url('users.get', \
			'user_ids=%s&fields=%s' % (uid, fields))).json()
		
		if 'error' in result.keys():
			raise VkException('Error message: %s Error code: %s' % \
				(result['error']['error_msg'], result['error']['error_code']))
		
		return result['response']


	def get_friends_list(self, uid):
		""" Returns user's friend list
		"""
		result = requests.get(self._get_request_url('friends.get', \
			'user_id=%s' % uid)).json()

		return result['response']['items']


	def get_users_from_group(self, group, count, city=''):
		""" Returns a `count` of users from `group` and `city`
		"""
		result = list()
		offset = 0
		current = 0

		while current in range(count):
			get_count = lambda: count if 1000 - count >= 0 else \
						count - current if count - current <= 1000 else \
						1000
			tmp = requests.get(self._get_request_url('groups.getMembers', \
				'group_id=%s&fields=city,photo&count=%s&offset=%s' % (group, \
					get_count(), offset), access_token=True))\
			.json()['response']['items']
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
		result = requests.get(self._get_request_url('database.getCountries', \
			'need_all=1&code=%s' % code)).json()

		return result['response']['items']


	def get_regions(self, country):
		""" Returns a country's regions list
		"""
		result = requests.get(self._get_request_url('database.getRegions', \
			'country_id=%s' % country)).json()

		return result['response']['items']


	def get_cities(self, country, region='', count=1000, get_all=False):
		""" Returns a country's cities list
		"""
		result = list()
		offset = 0
		current = 0
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