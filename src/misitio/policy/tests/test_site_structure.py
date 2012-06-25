import unittest2 as unittest

from Products.CMFCore.utils import getToolByName

from misitio.policy.testing import\
    MISITIO_POLICY_INTEGRATION_TESTING


class TestSiteStructure(unittest.TestCase):

    layer = MISITIO_POLICY_INTEGRATION_TESTING
    
    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']

    def test_default_content_is_removed(self):
        existing = self.portal.objectIds()
        self.assertTrue('events' not in existing)
        self.assertTrue('font-page' not in existing)
        self.assertTrue('news' not in existing)        
        self.assertTrue('Member' not in existing)

    def test_misitio_site_structure_is_create(self):

        existing = self.portal.objectIds()

        self.assertTrue('twitter' in existing)
        self.assertTrue('facebook' in existing)

        self.assertTrue('acerca-de' in existing)
        folder = self.portal['acerca-de'].objectIds()
        self.assertTrue('tu-compania' in folder)
        self.assertTrue('ubicacion' in folder)


        self.assertTrue('servicios' in existing) 
        folder = self.portal['servicios'].objectIds()
	self.assertTrue('consultoria' in folder) 
        self.assertTrue('capacitacion' in folder)
        self.assertTrue(self.portal.restrictedTraverse('servicios/capacitacion/plone'))
        self.assertTrue(self.portal.restrictedTraverse('servicios/capacitacion/python'))
        

        



