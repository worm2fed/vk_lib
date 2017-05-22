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


import requests

from parser import *
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
	def __init__(self, api_v, app_id, token):
		""" Initialisation

			:param api_v: VK API version
			:param api_id: VK app id
			:param token: access token
    	"""
		self.api_v 	= api_v
		self.app_id = app_id
		self.token 	= token
		

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


	def get_access_token_url(self):
		""" Returns url to get access token for current session

			**Note**
			When you are trying to use your previous access token from another
			IP adress you likely get an error. This function allows you to get 
			another access token
		"""
		return "https://oauth.vk.com/authorize?client_id={app_id}&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v={api_v}".format(
			app_id=self.app_id, api_v=self.api_v)


	def get_user_info(self, uid, fields=''):
		""" Returns user/users profile info with `fields`

			:param uid: user id
			:param fields: fields wich are needed to get
		"""
		result = requests.get(self._get_request_url('users.get', \
			'user_ids=%s&fields=%s' % (uid, fields))).json()

		if 'error' in result.keys():
			raise VkException('Error message: %s Error code: %s' % \
				(result['error']['error_msg'], result['error']['error_code']))
		
		return result['response']


	def get_friends(self, uid, city=''):
		""" Returns user's friend list

			:param uid: user id to get friends list
			:param city: city id to filter results
		"""
		result = []
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

		return result


	def get_friends_list(self, uid, city=''):
		""" Returns user's friend list

			:param uid: list of users id to get friends
			:param city: city id to filter results
		"""
		result = []
		if type(uid) is not list:
			raise VkException('Error message: %s' % \
					'uid should be <class \'list\'>')

		# разбиваем список на части - по 25 в каждой
		for p in make_parts(uid):
			tmp = requests.get(self._get_request_url('execute.getFriends', \
				'targets=%s' % make_targets(p), True)).json()

			if 'error' in tmp.keys():
				raise VkException('Error message: %s Error code: %s' % \
					(tmp['error']['error_msg'], tmp['error']['error_code']))
			tmp = tmp['response']
				
			for i, id in enumerate(p):
				# Check is user exactly in city
				if city:
					friends = []
					for u in tmp[i]['items']:
						if 'city' in u:
							if u['city']['id'] == city:
								friends.append(u)
				else:
					friends = tmp[i]['items']
						
				result.append({ id: friends })

		return result


	def get_followers(self, uid, city=''):
		""" Returns user's followers list

			:param uid: user id to get followers list
			:param city: city id to filter results
		"""
		result 	= []
		offset 	= 0
		current = 0

		while True:
			tmp = requests.get(self._get_request_url('users.getFollowers', \
				'user_id=%s&fields=city,photo&count=%s&offset=%s' % (uid, \
					1000, offset), access_token=True)).json()

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
				result 	+= tmp
				current += len(tmp)

		return result


	def get_users_from_group(self, group, count, city=''):
		""" Returns a `count` of users from `group` and `city`

			:param group: group id to search in
			:param count: nuber of users to get
			:param city: city id to filter results
		"""
		result 	= []
		offset 	= 0
		current = 0

		while current in range(count):
			get_count = lambda: count if 1000 - count >= 0 else \
						count - current if count - current <= 1000 else \
						1000
			tmp = requests.get(self._get_request_url('groups.getMembers', \
				'group_id=%s&fields=city,photo&count=%s&offset=%s' % (group, \
					get_count(), offset), access_token=True)).json()

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
		result = requests.get(self._get_request_url('database.getCountries', \
			'need_all=1&code=%s' % code)).json()

		return result['response']['items']


	def get_regions(self, country):
		""" Returns a country's regions list

			:param country: country id to get regions
		"""
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
		result 	= []
		offset 	= 0
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

		return result


	def get_all_valid_ids(self):
		""" This method parse vk.com/catalog to get all valid user's ids
		"""
		ids = []
		tags_x = [ { 'tag': 'a', 'attr': 'href', \
			'pattern': 'catalog\.php\?selection=[0-9]\d*' } ]
		pa_x = Parser('https://vk.com/catalog.php', tags_x)

		# Go though all links on /catalog.php?selection=X
		for x in pa_x.result['a']:
			tags_y = [ { 'tag': 'a', 'attr': 'href', \
				'pattern': 'catalog\.php\?selection=[0-9]\d*-[0-9]\d*' } ]
			pa_y = Parser('https://vk.com/' + x, tags_y)

			# Go though all links on /catalog.php?selection=X-Y
			for y in pa_y.result['a']:
				tags_z = [ { 'tag': 'a', 'attr': 'href', \
					'pattern': 'catalog\.php\?selection=[0-9]\d*-[0-9]\d*-[0-9]\d*' } ]
				pa_z = Parser('https://vk.com/' + y, tags_z)
				
				# Go though all links on /catalog.php?selection=X-Y-Z
				for z in pa_z.result['a']:
					tags_u = [ { 'tag': 'a', 'attr': 'href', \
						'pattern': 'id[0-9]\d*' } ]
					pa_u = Parser('https://vk.com/' + z, tags_u)

					# Go though all valid users
					for u in pa_u.result['a']:
						tags_id = [ { 'tag': 'a', 'attr': 'href', \
							'pattern': 'city' } ]
						pa_id = Parser('https://vk.com/' + u, tags_id)
						
						ids += pa_id.result['a']

		return ids