import time
import os
import sys
import json

import logger

try:
    import cherrypy
except:
    logger.log("error", "You need the CherryPy-module for this to work!", time.strftime("%c"))    
    exit()

try:
    from configobj import ConfigObj
except:
    logger.log("error", "You need the ConfigObj-module for this to work!", time.strftime("%c"))
    exit() 

try:
    from Cheetah.Template import Template
except:
    logger.log("error", "You need the Cheetah-module for this to work!", time.strftime("%c"))
    exit()

config = ConfigObj(os.path.join(sys.path[0], 'config'))

def get_real_dir(*dir):
    """
    Get the real directory path.
    """
    
    return os.path.join(sys.path[0], *dir)

def interface(title, content, error=''):
    path = get_real_dir('webdata', 'templates', 'layout.tmpl')

    info = {'title' : title,
            'content' : content,
            'error' : error}

    template = Template(file = path, searchList = [info])

    return template.respond()
