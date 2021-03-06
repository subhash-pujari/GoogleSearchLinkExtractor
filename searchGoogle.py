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
		#print str
		#get the index for '<' position
		startIndex = [a.start() for a in list(re.finditer('<', str))]

	#get the index for '>' position	
		endIndex = [a.end() for a in list(re.finditer('>', str))]
		shift = 0;
		#map both the list to remove the tags from the html page
		for i in range(len(startIndex)):
						
			if i > 0: 
				shift = shift + endIndex[i-1] - startIndex[i-1]
			start = startIndex[i] - shift
			end = endIndex[i] - shift
			str = str[0:start] + str[end:len(str)]
			#print str
		#return the extracted link		
		return str
		# print startIndex
		# print endIndex
	
		
# get search url list from google search API
def twitterLinkParser(data):

	listOfLink = list()
	soup = BeautifulSoup(data)
	#get all div tags in the page
	listOfTag = soup.find_all('div')
	for i in listOfTag:
		soup = BeautifulSoup(i.__str__())
		tag = soup.div
		#print type(tag)
		
		#check whether class attribute is present in the tag
		if 'class' in tag.attrs:
			#get value of class attribute		
			str = tag.attrs['class']
			# check if class is equal to kv			
			if 'kv' == str[0]:
				www = tag.cite
				if www:
#get the link out of content inside div
					listOfLink.append(remove_tags(www))
				#print True
		#else:
			#h2_headings.append('no id')
			#	print 'no id'

	return listOfLink

def twitterHandleExtractor(listOfLinks):

	twitterlinks = list()

	if listOfLinks:
		print 'listOfLinks not null'		
		for i in listOfLinks:
			if 'twitter.com' in i:
				twitterlinks.append(i)

	return twitterlinks

def main():
	
	fileCSV = open("../confList.csv")
	fileCSVtwitterConf = open("../twitterlist.csv", "w")
	for line in fileCSV:
		domainConf = line.split('\t')
		conf = domainConf[1]
		conf = conf[0:len(conf)-1]
		conf = conf.replace(' ', '+')
		conf = conf + '+twitter'
		#print conf
		url = protocol + base + url_type + query_argument + conf	
		#print url
		content = http.get(url)
		twitterLinks = twitterHandleExtractor(twitterLinkParser(content))
		if twitterLinks and len(twitterLinks)>0:
			for i in twitterLinks:
				string = domainConf[0] +'\t'+conf+'\t'+i+'\n'
				print string
				fileCSVtwitterConf.write(string)
	

if __name__ == "__main__":
	main()
