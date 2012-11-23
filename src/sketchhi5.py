import urllib2
import simplejson

search_string = 'wikipedia'
#url = ('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=blah')
url = ('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q='+search_string+'&userip=INSERT-USER-IP')
#url = ('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=blah&userip=INSERT-USER-IP')

request = urllib2.Request(url, None, {'Referer': 'google.com'})
response = urllib2.urlopen(request)

# Process the JSON string.
results = simplejson.load(response)
# now have some fun with the results...
print "done"