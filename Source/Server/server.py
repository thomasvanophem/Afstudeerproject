import geo_data
from functions import *
from web.index import Index

def main():
    geo_data.download_helper()
    cherry_conf = {'global': {
			'tools.sessions.on': True,
			'tools.sessions.timeout': 20160, #14 days
			'server.socket_host': '192.168.0.13',
			'tools.trailing_slash.on': False}
                    }

    cherrypy.quickstart(Index(), config = cherry_conf)

if __name__ == "__main__":
    main()
