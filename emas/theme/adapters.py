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

    def get_askanexpert_registrationdate(self):
        return self.context.getProperty('askanexpert_registrationdate', '')
    def set_askanexpert_registrationdate(self, value):
        return self.context.setMemberProperties({'askanexpert_registrationdate': value})
    askanexpert_registrationdate = property(get_askanexpert_registrationdate,
                                            set_askanexpert_registrationdate)

    def get_answerdatabase_registrationdate(self):
        return self.context.getProperty('answerdatabase_registrationdate', '')
    def set_answerdatabase_registrationdate(self, value):
        return self.context.setMemberProperties({'answerdatabase_registrationdate': value})
    answerdatabase_registrationdate = property(get_answerdatabase_registrationdate,
                                            set_answerdatabase_registrationdate)

    def get_moreexercise_registrationdate(self):
        return self.context.getProperty('moreexercise_registrationdate', '')
    def set_moreexercise_registrationdate(self, value):
        return self.context.setMemberProperties({'moreexercise_registrationdate': value})
    moreexercise_registrationdate = property(get_moreexercise_registrationdate,
                                            set_moreexercise_registrationdate)
