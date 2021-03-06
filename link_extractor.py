import os
import urllib
from bs4 import BeautifulSoup
from pygoogle import pygoogle
import re
def get_text(url):
	html = urllib.urlopen(url).read()
	soup = BeautifulSoup(html,'lxml')
	
	# kill all script and style elements
	for script in soup(["script", "style"]):
	    script.extract()    # rip it out
	
	# get text
	text = soup.get_text()
	
	# break into lines and remove leading and trailing space on each
	lines = (line.strip() for line in text.splitlines())
	# break multi-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	# drop blank lines
	text = '\n'.join(chunk for chunk in chunks if chunk)
	# use only if 600 characters or more
	return text
	
def main(query):
	g = pygoogle(query)
	g.pages = 1		# Get one page of results
	linkFile = open(os.path.join('data', 'linkFile'),'w')	# Store all search URLs
	count=0
	cleaner = re.compile('\[.*?\]')
	for url in g.get_urls():
		linkFile.write(url+'\n')
		target = open(os.path.join('data', query+'_'+str(count)+'.txt' ),'w')	# Create corresponding 'query_' + count filename
		#target.write(get_text(url).encode('ascii','ignore'))
		text = (get_text(url).encode('ascii','ignore'))
		for line in text.split('\n'):
			if len(line) > 600:
				line = re.sub(cleaner,'',line)
				if line[len(line)-1] == '.':
					target.write(line+'\n\n')
				else:
					target.write(line+'.\n\n')
		count = count + 1

if __name__ == '__main__':
	main(sys.argv)
