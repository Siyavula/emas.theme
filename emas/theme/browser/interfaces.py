from zope.interface import Interface

class ITOC(Interface):

    def toc():
        """ Table of Contents
        """


class ITOCView(Interface):
    """Interface to the view that creates a Table of Contents"""

    def createTOC():
        """Create the table of contents data structure"""

