import geo_data
from functions import *
from web.index import Index

def main():
    geo_data.download_helper()
    cherry_conf = {'global': {
			'tools.sessions.on': True,
			'tools.sessions.timeout': 20160, #14 days
			'server.socket_host': '192.168.0.13',
			'tools.trailing_slash.on': False},
                    '/css': {
                        'tools.staticdir.on': True,
                        'tools.staticdir.dir': "/home/thomas/Afstudeerproject/Source/Server/webdata/css"},
                    '/layout.css': {
                        'tools.staticfile.on': True,
                        'tools.staticfile.filename': "/home/thomas/Afstudeerproject/Source/Server/webdata/css/layout.css"}
                    }

    cherrypy.quickstart(Index(), config = cherry_conf)

if __name__ == "__main__":
    main()
