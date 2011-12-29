import logging
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.MimetypesRegistry.MimeTypeItem import MimeTypeItem
from Products.PortalTransforms.chain import chain

log = logging.getLogger('emas.theme-setuphandlers')

shortcodehtml = MimeTypeItem(name="text/shortcodehtml", 
                       mimetypes=("text/shortcodehtml",),
                       extensions=("shortcodehtml",),
                       binary="no",
                       icon_path="application.png")

shortcodecnxml = MimeTypeItem(name="application/shortcodecnxml+xml", 
                       mimetypes=("application/shortcodecnxml+xml",),
                       extensions=("shortcodecnxml",),
                       binary="no",
                       icon_path="application.png")

cnxmlplus = MimeTypeItem(name="application/cnxmlplus+xml", 
                       mimetypes=("application/cnxmlplus+xml",),
                       extensions=("cnxmlplus",),
                       binary="no",
                       icon_path="application.png")


def register_shortcode_html_mimetype(portal):
    registry = getToolByName(portal, 'mimetypes_registry')
    log.info('Intalling text/shortcodehtml mimetype')
    registry.register(shortcodehtml)
    log.info('Mimetype text/shortcodehtml installed successfully')

def register_shortcode_cnxml_mimetype(portal):
    registry = getToolByName(portal, 'mimetypes_registry')
    log.info('Intalling application/shortcodecnxml mimetype')
    registry.register(shortcodecnxml)
    log.info('Mimetype text/shortcodecnxml installed successfully')

def register_cnxmlplus_mimetype(portal):
    registry = getToolByName(portal, 'mimetypes_registry')
    log.info('Intalling application/cnxmlplus+xml mimetype')
    registry.register(cnxmlplus)
    log.info('Mimetype application/cnxmlplus+xml installed successfully')

def install_cnxmlplus_to_shortcodecnxml(portal):
    log.info('Installing cnxmlplus_to_shortcodecnxml transform')
    cnxmlplus_to_shortcodecnxml = 'cnxmlplus_to_shortcodecnxml'
    cnxmlplus_to_shortcodecnxl_module = "emas.theme.transforms.cnxmlplus2shortcodecnxml"
    pt = getToolByName(portal, 'portal_transforms')

    if cnxmlplus_to_shortcodecnxml not in pt.objectIds():
        pt.manage_addTransform(
            cnxmlplus_to_shortcodecnxml,
            cnxmlplus_to_shortcodecnxl_module)
    log.info('cnxmlplus_to_shortcodecnxl transform installed successfully.')

def install_shortcodehtml_to_html(portal):
    log.info('Installing shortcodehtml_to_html transform')
    shortcodehtml_to_html = 'shortcodehtml_to_html'
    shortcodehtml_to_html_module = "emas.theme.transforms.shortcodehtml2html"
    pt = getToolByName(portal, 'portal_transforms')

    if shortcodehtml_to_html not in pt.objectIds():
        pt.manage_addTransform(shortcodehtml_to_html, shortcodehtml_to_html_module)
    log.info('shortcodehtml_to_html transform installed successfully.')

def install_cnxmlplus_to_html(portal):
    log.info('Installing cnxmlplus_to_html transform')
    cnxmlplus_to_html = 'cnxmlplus_to_html'
    cnxmlplus_to_html_module = "emas.theme.transforms.cnxmlplus2html"
    pt = getToolByName(portal, 'portal_transforms')

    if cnxmlplus_to_html not in pt.objectIds():
        pt.manage_addTransform(cnxmlplus_to_html, cnxmlplus_to_html_module)
    log.info('cnxmlplus_to_html transform installed successfully.')

def install_shortcodecnxml_to_shortcodehtml(portal):
    log.info('Installing shortcodecnxml_to_shortcodehtml transform')
    shortcodecnxml_to_shortcodehtml = 'shortcodecnxml_to_shortcodehtml'
    shortcodecnxml_to_shortcodehtml_module = "emas.theme.transforms.shortcodecnxml2shortcodehtml"
    pt = getToolByName(portal, 'portal_transforms')

    if shortcodecnxml_to_shortcodehtml not in pt.objectIds():
        pt.manage_addTransform(
            shortcodecnxml_to_shortcodehtml,
            shortcodecnxml_to_shortcodehtml_module)
    log.info('shortcodecnxml_to_shortcodehtml transform installed successfully.')

def install_cnxmlplus_to_html_chain(portal):
    pt = getToolByName(portal, 'portal_transforms')
    chainid = 'cnxmlplus_to_html_chain'
    if chainid not in pt.objectIds():
        pt.manage_addTransformsChain(chainid, 'CNXML+ to HTML transforms')
        emas_chain = pt[chainid]
        emas_chain.manage_addObject('cnxmlplus_to_shortcodecnxml')
        emas_chain.manage_addObject('shortcodecnxml_to_shortcodehtml')
        emas_chain.manage_addObject('shortcodehtml_to_html')

def reorder_contenttype_registry(portal):
    registry = getToolByName(portal, 'content_type_registry')
    # move cnxml predicate to the top
    registry.reorderPredicate('cnxml', 0)

def install(context):
    if context.readDataFile('emas.theme-marker.txt') is None:
        return
    site = context.getSite()

    register_cnxmlplus_mimetype(site)
    register_shortcode_cnxml_mimetype(site)
    register_shortcode_html_mimetype(site)

    install_cnxmlplus_to_shortcodecnxml(site)
    install_shortcodecnxml_to_shortcodehtml(site)
    install_shortcodehtml_to_html(site)
    #install_cnxmlplus_to_html(site)
    install_cnxmlplus_to_html_chain(site)

    reorder_contenttype_registry(site)
