# -*- coding:  utf-8 -*-

import logging

from misitio.utilities.utility import createLink
from misitio.utilities.utility import createDocument
from misitio.utilities.utility import createFolder

logger = logging.getLogger('misitio.policy')

def remove_default_content(site):
    """Borra el contenido creado en la instalacion de plone"""
    removable = ['Members','news','events','front-page']
    for item in removable:
        if hasattr(site, item):
            site.manage_delObjects([item])

def create_site_structure(site) :
    """Crea la estructura del sitio Misitio."""
    createFolder(site, u'Acerca de', 
                 allowed_types=['Document','Folder'], 
                 exclude_from_nav=False)
    createFolder(site, u'Contactos', 
                 allowed_types=['Document','Folder','Image'], 
                 exclude_from_nav=False)
    createFolder(site, u'Servicios', 
                 allowed_types=['Document','Folder','Image','File'], 
                 exclude_from_nav=False)
    createLink(site, u'Twitter','www.twitter.com/vtvcanal8', 
               exclude_from_nav=False)
    createLink(site, u'Facebook','www.facebook.com/vtvcanal8', 
               exclude_from_nav=False)
    createDocument(site['acerca-de'], u'Tu Compania')
    createDocument(site['acerca-de'], u'Ubicacion')
    createDocument(site['servicios'], u'Consultoria')
    createFolder(site['servicios'], u'Capacitacion', 
                 allowed_types=['Document','Folder','Image','File'], 
                 exclude_from_nav=False)
    createDocument(site['servicios']['capacitacion'], u'Python')
    createDocument(site['servicios']['capacitacion'], u'Plone')   

def setupVarious(context):
    if context.readDataFile('misitio.policy-default.txt') is None:
        return
    portal = context.getSite()
    remove_default_content(portal)
    create_site_structure(portal)
