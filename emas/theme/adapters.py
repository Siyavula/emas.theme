from plone.app.users.browser.personalpreferences import UserDataPanelAdapter

class EmasUserDataPanelAdapter(UserDataPanelAdapter):

    def get_credits(self):
        return self.context.getProperty('credits', 0)
    def set_credits(self, value):
        return self.context.setMemberProperties({'credits': value})
    credits = property(get_credits, set_credits)

    def get_userrole(self):
        return self.context.getProperty('userrole', '')
    def set_userrole(self, value):
        return self.context.setMemberProperties({'userrole': value})
    userrole = property(get_userrole, set_userrole)

    def get_school(self):
        return self.context.getProperty('school', '')
    def set_school(self, value):
        return self.context.setMemberProperties({'school': value})
    school = property(get_school, set_school)

    def get_province(self):
        return self.context.getProperty('province', '')
    def set_province(self, value):
        return self.context.setMemberProperties({'province': value})
    province = property(get_province, set_province)

