import coordinate_calc

from functions import *

class Index():
    @cherrypy.expose
    def index(self, lat = None, lon = None, radius = None):
        if cherrypy.request.method == "GET":
            #return interface("Home", """<h2>Welkom!</h2>
            #                            <form method="POST" action="">
            #                            Latitude: <input type="text" name="lat" id="lat" /><br />
            #                            Longitude: <input type="text" name="lon" id="lon" /><br />
            #                            Radius in KM: <input type="text" name="radius" id="radius" /><br />
            #                            <input type="submit" value="Verzenden" />
            #                            </form>
            #                        """)
            return interface("Home", "")
        elif cherrypy.request.method == "POST":
            temp = coordinate_calc.main((lat, lon), radius)
            print json.dumps(temp)
            return json.dumps(temp)
	    #return return_results("""Latitude: %s <br />
            #                        Longitude: %s <br />
            #                        Radius: %s <br />
            #                        Cities: %s"""%(float(lat), float(lon), float(radius), temp))
            #return interface("Home", """<h2>Welkom!</h2>
            #                            Latitude: %s <br />
            #                            Longitude: %s <br />
            #                            Radius: %s <br/>
            #                            Steden: %s
            #                         """%(float(lat), float(lon), float(radius), temp))
