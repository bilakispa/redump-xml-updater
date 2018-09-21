import sys
from urllib.request import Request, urlopen
import urllib.parse
import socket
import re
import xml.etree.ElementTree as ET
import http.server
import socketserver

#Config
url = 'http://redump.org/'
regex = {
	'datfile' : r'<a href="/datfile/(.*?)">',
	'date' : r'\) \((.*?)\)\.',
	'name' : r'filename="(.*?) Datfile'
}
xml_filename = 'profile.xml'
server_address = '127.0.0.1'
server_port = 80

def Update_XML():
	print('Updating XML ...')
	
	print(' * Retrieving site info', end=' ')
	sys.stdout.flush()
	try:
		response = urlopen(url, timeout=30)
	except urllib.error.URLError:
		print('URL Error')
		quit()
	except socket.timeout:
		print('Socket timeout')
		quit()

	respData = response.read()
	
	print('(DONE)')
	print(' * Processing data', end=' ')
	sys.stdout.flush()
	
	datFiles = re.findall(regex['datfile'], str(respData))
	datInfo = []
	dict = {}
	for dat in datFiles:
		response = urlopen(Request(url+'datfile/'+dat, method='HEAD'))
		header = response.info()
		#get the date from the file name
		dict['Date'] = re.findall(regex['date'], header['Content-Disposition'])[0]
		
		#generate the dat's name
		tempName = re.findall(regex['name'], header['Content-Disposition'])[0]
		#trim the - from the end (if exists)
		if (tempName.endswith('-')):
			tempName = tempName[:-2]
		elif (tempName.endswith('BIOS')):
			tempName = tempName + ' Images'
		dict['Name'] = tempName
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
		ET.SubElement(tag_datfile, 'comment').text = '_'
		ET.SubElement(tag_datfile, 'url').text = '_'
		ET.SubElement(tag_datfile, 'file').text = '_'
		
	xmldata = ET.tostring(tag_clrmamepro).decode()
	xmlfile = open(xml_filename, 'w')
	xmlfile.write(xmldata)
	print('(DONE)')

def Start_Server():
	Handler = http.server.SimpleHTTPRequestHandler
	with socketserver.TCPServer((server_address, server_port), Handler) as httpd:
		print('Serving HTTP on ' + server_address + ' port ' + str(server_port) + ' (http://'+server_address+':'+str(server_port)+'/) ...')
		#httpd.serve_forever()
		try:
			httpd.serve_forever()
		except KeyboardInterrupt:
			print('Terminating server ...')
		finally:
			# Clean-up server (close socket, etc.)
			httpd.server_close()

print('Welcome to Redump.org XML updater')
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
	