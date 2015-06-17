"""
Implements the webserver using CherryPy.

python server.py to start the server.

Author: Thomas van Ophem, thomas.vanophem@student.uva.nl
Date: 26-04-2015
"""
import geo_data
from functions import *
from web.index import Index

def main():
    # Download the geo data.
    geo_data.download_helper()

    # CherryPy configuration.
    cherry_conf = {'global': {
                    'tools.sessions.on': True,
                    'tools.sessions.timeout': 20160, #14 days
                    'server.socket_host': '0.0.0.0',
                    'tools.trailing_slash.on': False},
                    '/css': {
                        'tools.staticdir.on': True,
                        'tools.staticdir.dir': "/home/thomas/Afstudeerproject/Source/Server/webdata/css"},
                    '/js': {
                        'tools.staticdir.on': True,
                        'tools.staticdir.dir': "/home/thomas/Afstudeerproject/Source/Server/webdata/js"},
                    '/img': {
                        'tools.staticdir.on': True,
                        'tools.staticdir.dir': "/home/thomas/Afstudeerproject/Source/Server/webdata/img"},
                    '/layout.css': {
                        'tools.staticfile.on': True,
                        'tools.staticfile.filename': "/home/thomas/Afstudeerproject/Source/Server/webdata/css/layout.css"},
                    '/maps.js': {
                        'tools.staticfile.on': True,
                        'tools.staticfile.filename': "/home/thomas/Afstudeerproject/Source/Server/webdata/js/maps.js"},
                    '/marker.png': {
                        'tools.staticfile.on': True,
                        'tools.staticfile.filename': "/home/thomas/Afstudeerproject/Source/Server/webdata/img/marker.png"}
                    }

    # Start the server using our own configuration.
    cherrypy.quickstart(Index(), config = cherry_conf)

if __name__ == "__main__":
    main()