import logging
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.MimetypesRegistry.MimeTypeItem import MimeTypeItem

log = logging.getLogger('emas.theme-setuphandlers')

shortcodehtml = MimeTypeItem(name="text/shortcodehtml", 
                       mimetypes=("text/shortcodehtml",),
                       extensions=("shortcodehtml",),
                       binary="no",
                       icon_path="application.png")

cnxmlplus = MimeTypeItem(name="application/cnxmlplus+xml", 
                       mimetypes=("application/cnxmlplus+xml",),
                       extensions=("cnxmlplus",),
                       binary="no",
                       icon_path="application.png")


def register_shortcode_html(portal):
    registry = getToolByName(portal, 'mimetypes_registry')
    log.info('Intalling text/shortcodehtml mimetype')
    registry.register(shortcodehtml)
    log.info('Mimetype text/shortcodehtml installed successfully')

def register_cnxmlplus_mimetype(portal):
    registry = getToolByName(portal, 'mimetypes_registry')
    log.info('Intalling application/cnxmlplus+xml mimetype')
    registry.register(cnxmlplus)
    log.info('Mimetype application/cnxmlplus+xml installed successfully')

def install_cnxmlplus_to_cnxml(portal):
    log.info('Installing cnxmlplus_to_cnxml transform')
    cnxmlplus_to_cnxml = 'cnxmlplus_to_cnxml'
    cnxmlplus_to_cnxl_module = "emas.theme.transforms.cnxmlplus2cnxml"
    pt = getToolByName(portal, 'portal_transforms')

    if cnxmlplus_to_cnxml not in pt.objectIds():
        pt.manage_addTransform(cnxmlplus_to_cnxml, cnxmlplus_to_cnxl_module)
    log.info('cnxmlplus_to_cnxl transform installed successfully.')

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
    cnxmlplus_to_html_module = "emas.transforms.cnxmlplus2html"
    pt = getToolByName(portal, 'portal_transforms')

    if cnxmlplus_to_html not in pt.objectIds():
        pt.manage_addTransform(cnxmlplus_to_html, cnxmlplus_to_html_module)
    log.info('cnxmlplus_to_html transform installed successfully.')

def reorder_contenttype_registry(portal):
    registry = getToolByName(portal, 'content_type_registry')
    # move cnxml predicate to the top
    registry.reorderPredicate('cnxml', 0)

def install(context):
    if context.readDataFile('emas.theme-marker.txt') is None:
        return
    site = context.getSite()
    register_cnxmlplus_mimetype(site)
    install_cnxmlplus_to_cnxml(site)
    #register_shortcode_html(site)
    #install_cnxmlplus_to_html(site)
    reorder_contenttype_registry(site)
