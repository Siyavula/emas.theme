from five import grok
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName

from emas.theme.interfaces import IEmasThemeLayer

MATHS_EXAM_PAPERS_GROUP = "PastMathsExamPapers"
SCIENCE_EXAM_PAPERS_GROUP = "PastScienceExamPapers"

SUBJECT_MAP = {
    'maths': MATHS_EXAM_PAPERS_GROUP,
    'science': SCIENCE_EXAM_PAPERS_GROUP,
}


grok.templatedir('templates')
grok.layer(IEmasThemeLayer)


class MXitStats(grok.View):
    """
        Custom view for mxit signup stats 
    """

    grok.context(Interface)
    grok.require('zope2.View')
    
    def stats_per_group(self):
        group_stats = {}
        gt = getToolByName(self.context, 'portal_groups')
        for groupname in SUBJECT_MAP.values():
            group = gt.getGroupById(groupname)
            count = len(group.getMemberIds())
            group_stats[groupname] = count

        return group_stats
