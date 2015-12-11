import cgi
from google.appengine.api import users
import webapp2
from google.appengine.api import urlfetch
import json

MAIN_PAGE_HTML = """\
<!doctype html>
<html>
<link type="text/css" rel="stylesheet" href="/stylesheets/main.css">
	<head><meta name="viewport" content="width=device-width"></head>
		<body>
			<form action="/bikes" method="get">
				<div class= "center"><button type="submit" class="myButton">Get Bikes</button></div>
			</form>
		</body>
</html>
"""


class MainPage(webapp2.RequestHandler):

    def get(self):
		self.response.write(MAIN_PAGE_HTML)


class GetBikes(webapp2.RequestHandler):

    def get(self):
		self.response.write('<!doctype html><html><head><link type="text/css" rel="stylesheet" href="/stylesheets/main.css"><meta name="viewport" content="width=device-width"></head><body><div class= "center"><div class="roundbox"><h2>Stations that are more than half full</br></h2><p>The darker the row the closer that station is to being full</p></div><pre>\n<table style="width:300px">')
		url = "http://citibikenyc.com/stations/json"
		result = urlfetch.fetch(url=url,method=urlfetch.GET)
		if result.status_code != 200:
			self.response.write("url broken")
		dict = json.loads(result.content)
		for (x) in dict['stationBeanList']:
			if x['availableDocks'] < x['availableBikes']:
				lat = float(x['latitude'])
				long = float(x['longitude'])
				name = x['stationName']
				open = int(x['availableDocks'])
				total = float(x['availableDocks']) + int(x['availableBikes'])
				howfull = int((open/total)*256)
				self.response.write('<tr style="background-color: rgb(%d,%d,%d);"><td>' % (howfull,howfull,howfull))
				if howfull == 0:
					self.response.write('<a href="http://maps.google.com/?q=%f,%f">%s (FULL)</a></tr></td>\n' % (lat, long, name))
				else:
					self.response.write('<a href="http://maps.google.com/?q=%f,%f">%s</a></tr></td>\n' % (lat,long, name))			
		self.response.write('</table></pre></div></body></html>')


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/bikes', GetBikes),
], debug=True)