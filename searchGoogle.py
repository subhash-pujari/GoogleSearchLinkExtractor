from bs4 import BeautifulSoup
import http
import re

protocol = "http://"
base = "www.google.com"
url_type = "/search?"
query_argument = "q="
query_str = "international+conference+programming+language+twitter"

def remove_tags(link):

	if link:
		str = link.__str__()
		print str
		#get the index for <h2>
		startIndex = [a.start() for a in list(re.finditer('<', str))]

	#get the index for </h2>	
		endIndex = [a.end() for a in list(re.finditer('>', str))]
		shift = 0;
		for i in range(len(startIndex)):
						
			if i > 0: 
				shift = shift + endIndex[i-1] - startIndex[i-1]
			start = startIndex[i] - shift
			end = endIndex[i] - shift
			str = str[0:start] + str[end:len(str)]
			#print str
		return str
		# print startIndex
		# print endIndex
	
		
# get search url list from google search API
def twitterLinkParser(data):

	listOfLink = list()
	soup = BeautifulSoup(data)
	listOfTag = soup.find_all('div')
	for i in listOfTag:
		soup = BeautifulSoup(i.__str__())
		tag = soup.div
		#print type(tag)
		
		#check whether class attribute is present
		if 'class' in tag.attrs:
			#get class string			
			str = tag.attrs['class']
			# check if it is equal to kv			
			if 'kv' == str[0]:
				www = tag.cite
				if www:
					listOfLink.append(remove_tags(www))
				#print True
		#else:
			#h2_headings.append('no id')
			#	print 'no id'

	print listOfLink


def main():
	url = protocol + base + url_type + query_argument + query_str	
	print url
	content = http.get(url)
	twitterLinkParser(content)

if __name__ == "__main__":
	main()
