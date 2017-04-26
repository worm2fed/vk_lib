import requests

url = 'https://vk.com/catalog.php'
r = requests.get(url)

with open('catalog.html', 'w') as output_file:
	output_file.write(r.text.encode('utf-8'))