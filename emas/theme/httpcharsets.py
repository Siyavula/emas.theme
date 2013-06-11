from zope.publisher.http import HTTPCharsets

class MoreCharsets(HTTPCharsets):

    def getPreferredCharsets(self):
        charsets = super(MoreCharsets, self).getPreferredCharsets()
        if 'latin-1' not in charsets:
            charsets.append('latin-1')
        return charsets
