import os
import urllib
import re
from pygoogle import pygoogle
print "Enter search key word: "
query = raw_input()
g = pygoogle(query)
g.pages = 1		# Get one page of results
linkFile = open(os.path.join('data', 'linkFile'),'w')	# Store all search URLs
count=0
for url in g.get_urls():
	linkFile.write(url+'\n')
	htmlfile = urllib.urlopen(url)	# Open URL to read
	htmltext=htmlfile.read()
	target = open(os.path.join('data', query+'_'+str(count)+'.txt' ),'w')	# Create corresponding 'query_' + count filename
	for para in re.findall('<p>(.*?)</p>', htmltext, re.DOTALL):
		target.write(re.sub("(\<.*?\>)", "",para)+'\n')		# Write individual paragraphs
	count = count + 1
