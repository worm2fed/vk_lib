import sys
import requests
import pickle
import time

from graph_tool.all import *
from glob import glob
from settings import *

# Class to elapse time
class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()
         
    def __exit__(self, type, value, traceback):
        print('Elapsed time: {:.3f} sec '.format(time.time() - self._startTime))

# Class with Vk exception
class VkException(Exception):
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message

# Dictionaries for indexing vertecies
id_to_vertex = dict()
vertex_to_id = dict()		

# Class with Vk tools
class VkTools():
	# Initialisation
	def __init__(self, *pargs):
		self.api_v, self.token, self.count, self.city, self.fields, self.group = pargs
		
	# Generate request URL
	def get_request_url(self, method_name, parameters, access_token=False):
		request_url = 'https://api.vk.com/method/{method_name}?{parameters}&v={api_v}'.format(
			method_name=method_name, api_v=self.api_v, parameters=parameters)

		# Add access token if needed
		if access_token:
			request_url = '{}&access_token={token}'.format(request_url, token=self.token)

		return request_url

	# Get user info
	def get_user_info(self, uid):
		result = requests.get(self.get_request_url('users.get', 'user_ids=%s&fields=%s' % (uid, self.fields))).json()
		
		if 'error' in result.keys():
			raise VkException('Error message: %s Error code: %s' % (result['error']['error_msg'], result['error']['error_code']))
		
		result = result['response'][0]
		
		# Check is user deactivated
		# if 'deactivated' in result.keys():
		# 	raise VkException("User deactivated")

		return result

	# Get user's friend list
	def get_friends_list(self, uid):
		result = requests.get(self.get_request_url('friends.get', 'user_id=%s' % uid)).json()

		return result['response']['items']

	# Search users
	def search_users(self):
		global id_to_vertex
		global vertex_to_id
		result = set()
		offset = 0
		current = 0

		# Vk API has a count 1000 records at once,
		# so we have to use offset
		# while offset < count:
		while current < self.count:
			# Get user list
			tmp = requests.get(self.get_request_url('groups.getMembers', 'group_id=%s&fields=city&count=%s&offset=%s' % (self.group, 1000, offset), access_token=True)).json()['response']['items']

			if len(tmp) == 0:
				break

			# Sleep for a second 
			if offset % 3000 == 0:
				time.sleep(1)
			
			# Check is user in city
			for i in tmp:
				if 'city' in i:
					if i.get('city').get('id') == self.city:
						result.add(i.get('id'))
						id_to_vertex[i.get('id')] = current
						vertex_to_id[current] = i.get('id')
						current += 1

						if current >= self.count:
							break

			offset += 1000

		# Returns set with user's ids
		return result

	# Build grapg
	def build_graph(self, users):
		global id_to_vertex
		global vertex_to_id
		result = Graph(directed=False)
		edges = set()

		# Add edges and vertices
		for user in users:
			friends = self.get_friends_list(user)

			for friend in friends:
				if friend in users:
					if not (id_to_vertex[friend], id_to_vertex[user]) in edges:
						edges.add((id_to_vertex[user], id_to_vertex[friend]))
						result.add_edge(id_to_vertex[user], id_to_vertex[friend], add_missing=True)

		# Add additional info to vertices
		result.vertex_properties['id'] = result.new_vertex_property('int')
		for v in result.vertices():
			result.vertex_properties['id'][v] = vertex_to_id[result.vertex_index[v]]

		return result

if __name__ == '__main__':
	vk_tools = VkTools(api_v, token, count, city, fields, group)
	# If there are no graph - create it
	if not glob('graph.xml'):
		print('Collecting ' + str(count) + ' users from group ' + str(group) + ' and city ' + str(city) + '\nVK API version ' + str(api_v))

		print('\nStart searching...')
		users = vk_tools.search_users()
		print('Done!')
		print('\n'+ str(len(users)) + ' users were found')

		print('\n' + 'Get connections...')
		with Profiler() as p:
			graph = vk_tools.build_graph(users)
		print('Done!')
		
		print('Saving to file...')
		graph.save('graph.xml')
	# Else print it
	else:
		graph = load_graph('graph.xml')
		print('Vertices: ' + str(graph.num_vertices()) + ' Edges: ' + str(graph.num_edges()))
		
		print('\n' + 'Print graph...')
		with Profiler() as p:
			graph_draw(graph, pos=arf_layout(graph, max_iter=0), output_size=(1920, 1080), output="graph.png")
