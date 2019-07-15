import handy
from lxml import html
import requests
from urllib2 import urlopen, Request
from bs4 import BeautifulSoup
from handy import replace_all

def read_wordlist(fileName):
	fileObj = open(fileName, 'r')
	lines = fileObj.readlines()
	words = handy.flatten([x.split() for x in lines])
	words = [x for x in words if x != '']
	return words

def scrape(webpage, treeArgs):
	page = requests.get(webpage)
	tree = html.fromstring(page.content)
	stuff = tree.xpath(treeArgs)
	return stuff

#testScrape = scrape('http://harrypotter.wikia.com/wiki/List_of_spells', "//span[@class='mw-headline']")
#print testScrape[0]

def soupScrape(webpage):
	req = Request(webpage, headers={'User-Agent': 'Magic Browser'})	
	page = urlopen(req)
	soup = BeautifulSoup(page, 'lxml')
	return soup

tmp = open('idioms_temp.txt', 'a')
letter = 'xyz'
url = 'http://www.idiomconnection.com/{}quiz.html'.format(letter)
soup = soupScrape(url)
headers = [x.string for x in soup.find_all('b') if x.string != None]
headers.pop(0)
for x in headers:
	tmp.write(x.lower().capitalize().encode('utf-8'))
	tmp.write('\n')
tmp.close()
'''
letters = 'abcdefghijklmnopqrstuvw'
for letter in letters:
	url = 'http://www.idiomconnection.com/{}quiz.html'.format(letter)
	charSoup = soupScrape(url)
	chars = [char.string.strip(' 1234567890') for char in charSoup.find_all('strong') if char.string != None]
	filteredChars = [char for char in chars if char.startswith('.')]
	tmp = open('idioms_temp.txt', 'w')
	for x in filteredChars:
		tmp.write(x.strip('. ').replace(':','').lower().capitalize().encode('utf-8'))
		tmp.write('\n')
	tmp.close()
'''
