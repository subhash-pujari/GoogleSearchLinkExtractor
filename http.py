import urllib2
# this module is for http client

def get(url):
	request = urllib2.Request( url , headers={'User-Agent' : "Magic Browser"})
	f = urllib2.urlopen(request)
	return f.read()		

