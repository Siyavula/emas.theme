from plone.app.users.browser.personalpreferences import UserDataPanelAdapter

class EmasUserDataPanelAdapter(UserDataPanelAdapter):
    credits = property(
        lambda s: s.context.getProperty('credits'),
        lambda s, v: s.context.setProperties({'credits': v}))
