#! C:\python

import urllib2, binascii, json, os.path, webbrowser
# https://pypi.python.org/pypi/colorama
from colorama import init, Fore

# ------------------------------

init()	# init colorama

# Where to store the data from last fetch and current one
DATAFILENAME = 'change_detector_data.json'
# newline-separated URLs to track
URLSFILENAME = 'urls.txt'

def CRC32(content):
	return ("%08X" % (binascii.crc32(content) & 0xFFFFFFFF))

def SaveData(data, fileName):
	dataFile = file(fileName,'wt')
	dataFile.write(json.dumps(data))
	dataFile.close()

def LoadData(fileName):
	if os.path.isfile(fileName):
		dataFile = file(fileName,'rt')
		loadedData = dataFile.read()
		dataFile.close()
		loadedData = json.loads(loadedData)
	else:
		loadedData = {}
	return loadedData

def LoadURLs(fileName):
	if os.path.isfile(fileName):
		with open(fileName) as dataFile:
			urls = dataFile.readlines()
	else:
		urls = []
	return urls

def AddNewUrls(urls, data):
	for url in urls:
		if not CRC32(url) in data:
			data[CRC32(url)] = {
				'url' : url.rstrip('\n'),
				'crc_content' : None
			}
	return data

def FetchUrl(url):
	webpage = None
	try:
		urlFetcher = urllib2.urlopen(url, timeout=10)
		statusCode = urlFetcher.getcode()
		if statusCode == 200:
			webpage = CRC32(urlFetcher.read())
	except urllib2.URLError:
		statusCode = ''
	return { 'code' : statusCode, 'crc' : webpage }

def CheckForNews(data):
	for item in data:
		result = FetchUrl(data[item]['url'])
		if result['code'] == 200:
			if data[item]['crc_content'] == None:
				print Fore.YELLOW + u"NEW: %s" % (data[item]['url'])
			elif data[item]['crc_content'] == result['crc']:
				print Fore.CYAN + u"UNMODIFIED: %s" % (data[item]['url'])
			elif data[item]['crc_content'] != result['crc']:
				print Fore.GREEN + u"MODIFIED: %s" % (data[item]['url'])
				webbrowser.open(data[item]['url'])
			data[item]['crc_content'] = result['crc']
		else:
			print Fore.RED + u"ERROR: %s" % (data[item]['url'])
	return data

# ------------------------------

data = AddNewUrls(LoadURLs(URLSFILENAME), LoadData(DATAFILENAME))
data = CheckForNews(data)
SaveData(data, DATAFILENAME)
userInput = raw_input(Fore.WHITE + "FINISHED - Press [ENTER] key to close")