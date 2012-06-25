from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile
from zope.configuration import xmlconfig
from plone.testing import z2
from misitio.policy.config import PRODUCT_DEPENDENCIES

class MisitioPolicy(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import misitio.policy
        xmlconfig.file('configure.zcml',
                       misitio.policy,
                       context=configurationContext)
	z2.installProduct(app, 'Products.CMFPlacefulWorkflow')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'misitio.policy:default')



MISITIO_POLICY_FIXTURE = MisitioPolicy()
MISITIO_POLICY_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(MISITIO_POLICY_FIXTURE, ),
                       name="MisitioPolicy:Integration")
