import sys
import os
import xml.etree.ElementTree as ET
import re
import requests
import http.server
import socketserver

#Config
userinfo_filename = 'UserInfo.xml'
url_datfile = 'http://redump.org/datfile/'
url_downloads = 'http://redump.org/downloads/'
url_login = 'http://forum.redump.org/login/'
regex = {
	'datfile' : r'<a href="/datfile/(.*?)">',
	'date' : r'\) \((.*?)\)\.',
	'filename' : r'filename="(.*?)"',
	'name' : r'filename="(.*?) Datfile',
	'csrf' : r'csrf_token" value="(.*?)"'
}

xml_filename = 'profile.xml'
server_address = '127.0.0.1'
server_port = 8668

def Update_XML():
	print('Updating XML:')
	print(' * Retrieving site info', end=' ')
	sys.stdout.flush()
	
	#Get user info
	doLogin = 0
	username = ''
	password = ''
	if os.path.exists(userinfo_filename):
		#Check if is empty
		try:    
			tree = ET.parse(userinfo_filename)
			root = tree.getroot()
			username = root[0].text
			password = root[1].text
			if (username != None and password != None):
				doLogin = 1
		except ET.ParseError: #XML file is empty
			pass
	
	client = requests.session()
	if (doLogin == 1):
		#Retrieve the csrf token
		try:
			result = client.get(url_login)
		except requests.exceptions.RequestException as e:
			print ('Error: ')
			print (e)
			sys.exit(1)
		
		csrf_token = re.findall(regex['csrf'], str(result.text))[0]
		
		#Send a POST request to login
		payload = {
			'form_sent' : '1',
			'redirect_url' : url_downloads,
			'csrf_token' : csrf_token,
			'req_username' : username,
			'req_password' : password,
			'save_pass' : '0',
			'login' : 'Login'
		}
	
		header = {'User-Agent': 'Mozilla/5.0', 'referer': url_login}
		try:
			result = client.post(url_login, data=payload, headers=header)
		except requests.exceptions.RequestException as e:
			print ('Error: ')
			print (e)
			sys.exit(1)
	else:
		try:
			result = client.get(url_downloads)
		except requests.exceptions.RequestException as e:
			print ('Error: ')
			print (e)
			sys.exit(1)
	
	print('(DONE)')
	print(' * Processing data', end=' ')
	sys.stdout.flush()
	
	datFiles = re.findall(regex['datfile'], str(result.text))
	datInfo = []
	dict = {}
	for dat in datFiles:
		response = client.head(url_datfile + dat)
		content_header = response.headers['Content-Disposition']

		#get the date from the file name
		dict['Date'] = re.findall(regex['date'], content_header)[0]
		
		#generate the dat's name
		tempName = re.findall(regex['name'], content_header)[0]
		#trim the - from the end (if exists)
		if (tempName.endswith('-')):
			tempName = tempName[:-2]
		elif (tempName.endswith('BIOS')):
			tempName = tempName + ' Images'
		dict['Name'] = tempName

		dict['URL'] = url_datfile + dat
		
		filename = re.findall(regex['filename'], content_header)[0]
		if (filename.endswith('.zip')):
			filename = filename[:-3] + 'dat' # replace with .dat
		else:
			filename = ''
		dict['File'] = filename

		datInfo.append(dict.copy())
	
	print('(DONE)')
	print(' * Writing to ' + xml_filename, end=' ')
	sys.stdout.flush()
	
	tag_clrmamepro = ET.Element('clrmamepro')
	for info in datInfo:
		tag_datfile = ET.SubElement(tag_clrmamepro, 'datfile')
		ET.SubElement(tag_datfile, 'name').text = info['Name']
		ET.SubElement(tag_datfile, 'description').text = info['Name']
		ET.SubElement(tag_datfile, 'version').text = info['Date']
		ET.SubElement(tag_datfile, 'author').text = 'redump.org'
		ET.SubElement(tag_datfile, 'comment').text = ''
		ET.SubElement(tag_datfile, 'url').text = info['URL']
		ET.SubElement(tag_datfile, 'file').text = info['File']
		
	xmldata = ET.tostring(tag_clrmamepro).decode()
	xmlfile = open(xml_filename, 'w')
	xmlfile.write(xmldata)
	print('(DONE)')

def Start_Server():
	print('Starting Local Server:')
	Handler = http.server.SimpleHTTPRequestHandler
	with socketserver.TCPServer((server_address, server_port), Handler) as httpd:
		print('Serving HTTP on ' + server_address + ' port ' + str(server_port) + ' (http://'+server_address+':'+str(server_port)+'/) ...')
		try:
			httpd.serve_forever()
		except KeyboardInterrupt:
			print('Terminating server ...')
		finally:
			# Clean-up server (close socket, etc.)
			httpd.shutdown()
			httpd.server_close()

print('Welcome to Redump.org XML updater [Github: bilakispa/redump-xml-updater]')
try:
	option = input('1: Update XML & Run Local Server\n2: Update XML\n3: Run Local Server\n')
	while(option != '1' and option != '2' and option != '3' and option != ''):
		option = input('Please select a valid option [1,3] (Press enter to exit): ')
	
	if(option == '1'):
		Update_XML()
		Start_Server()
	elif(option == '2'):
		Update_XML()
	elif(option == '3'):
		Start_Server()
except KeyboardInterrupt:
	pass
