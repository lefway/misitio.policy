# -*- coding:  utf-8 -*-

import logging

from plone.i18n.normalizer import idnormalizer #sirve para normalizar el lenguaje
from Products.ATContentTypes.lib import constraintypes #retrige el tipo de contenido a una carpeta
from Products.CMFPlacefulWorkflow.PlacefulWorkflowTool import WorkflowPolicyConfig_id
from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('misitio.policy')

def remove_default_content(site):
    """Borra el contenido creado en la instalacion de plone"""
    removable = ['Members','news','events','front-page']
    for item in removable:
        if hasattr(site, item):
            site.manage_delObjects([item])

def set_workflow_policy(obj):
    """Cambiar el workflow del objeto utilizando CMFPlacefulWorkflow.
    """
    product = 'CMFPlacefulWorkflow'
    obj.manage_addProduct[product].manage_addWorkflowPolicyConfig()
    pc = getattr(obj, WorkflowPolicyConfig_id)
    pc.setPolicyIn(policy='one-state')
    logger.info('Workflow changed for element %s' % obj.getId())

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
    

def createLink(context,title,link,
               exclude_from_nav=False):
    """Crea y publica un vinculo en el contexto dado"""
    oid = idnormalizer.normalize(title, 'es')
    if not hasattr(context, oid):
        context.invokeFactory('Link', id=oid, title=title, remoteUrl=link)
        link = context[oid]
        if exclude_from_nav:
            link.setExcludeFromNav(True)
        link.reindexObject()

def createDocument(context, title):
    """Crea y publica un documento (página) en el contexto dado.
    """
    oid = idnormalizer.normalize(title, 'es')
    if not hasattr(context, oid):
        context.invokeFactory('Document', id=oid, title=title)
        document = context[oid]
        document.reindexObject()

def createFolder(context, title, allowed_types=['Topic', 'Folder', 'Document'],
                 exclude_from_nav=False):
    """Crea una carpeta en el contexto especificado y modifica su política de
    workflows; por omisión, la carpeta contiene colecciones (Topic) y no
    modifica la política de workflow del contenido creado dentro de ella.
    """
    oid = idnormalizer.normalize(title, 'es')
    if not hasattr(context, oid):
        context.invokeFactory('Folder', id=oid, title=title)
        folder = context[oid]
        folder.setConstrainTypesMode(constraintypes.ENABLED)
        folder.setLocallyAllowedTypes(allowed_types)
        folder.setImmediatelyAddableTypes(allowed_types)
        set_workflow_policy(folder)
        if exclude_from_nav:
            folder.setExcludeFromNav(True)
        folder.reindexObject()
    else:
        folder = context[oid]
        folder.setLocallyAllowedTypes(allowed_types)
        folder.setImmediatelyAddableTypes(allowed_types)
        # reindexamos para que el catálogo se entere de los cambios
        folder.reindexObject()

def setupVarious(context):
    if context.readDataFile('misitio.policy-default.txt') is None:
        return
    portal = context.getSite()
    remove_default_content(portal)
    create_site_structure(portal)
