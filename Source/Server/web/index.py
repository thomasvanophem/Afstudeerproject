"""
Implements a webpage using CherryPy and a Cheetah template.
"""
import geo_data

from functions import *

class Index():
    @cherrypy.expose
    def index(self, lat = None, lon = None, radius = None):
        if cherrypy.request.method == "GET":
            return interface("Home", "")
        elif cherrypy.request.method == "POST":
            if type(lat) == float and type(lon) == float and type(radius) == float:
                temp = geo_data.main("geo_data.db", (lat, lon), radius)
            else:
                temp = []

            return json.dumps(temp)