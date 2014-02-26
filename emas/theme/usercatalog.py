from persistent import Persistent
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.interface import Interface
from zope.interface import implements
from zope.intid import IIntIds
from zope.index.text.textindex import TextIndex

class IUserCatalog(Interface):
    """ Index and search on user's login, full name and email 
    """

class UserCatalog(Persistent):

    implements(IUserCatalog)

    def __init__(self):
        self._index = TextIndex()

    def index(self, member):
        ints = getUtility(IIntIds)  
        memberid = ints.register(member)
        text = "%s %s %s" % (member.getUserName(),
                             member.getProperty('fullname'),
                             member.getProperty('email'))
        self._index.index_doc(memberid, text)

    def unindex(self, member):
        ints = getUtility(IIntIds)  
        memberid = ints.register(member)
        self._index.unindex_doc(memberid)

    def search(self, searchstring):
        ints = getUtility(IIntIds)  
        result = []
        for k, v in self._index.apply(searchstring).items():
            result.append(ints.getObject(k))
        return result
             
