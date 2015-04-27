import coordinate_calc

from functions import *

class Index():
    @cherrypy.expose
    def index(self, lat = None, lon = None, radius = None):
        if cherrypy.request.method == "GET":
            return interface("Home", "")
        elif cherrypy.request.method == "POST":
            temp = coordinate_calc.main("geo_data.db", (lat, lon), radius)

            return json.dumps(temp)
