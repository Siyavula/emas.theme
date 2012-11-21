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
        return self._getProperty('school')
    def set_school(self, value):
        return self.context.setMemberProperties({'school': value})
    school = property(get_school, set_school)

    def get_province(self):
        return self._getProperty('province')
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

    def get_moreexercise_expirydate(self):
        return self.context.getProperty('moreexercise_expirydate', '')
    def set_moreexercise_expirydate(self, value):
        return self.context.setMemberProperties({'moreexercise_expirydate': value})
    moreexercise_expirydate = property(get_moreexercise_expirydate,
                                       set_moreexercise_expirydate)

    def get_answerdatabase_expirydate(self):
        return self.context.getProperty('answerdatabase_expirydate', '')
    def set_answerdatabase_expirydate(self, value):
        return self.context.setMemberProperties({'answerdatabase_expirydate': value})
    answerdatabase_expirydate = property(get_answerdatabase_expirydate,
                                         set_answerdatabase_expirydate)

    def get_intelligent_practice_access(self):
        return self.context.getProperty('intelligent_practice_access', '')
    def set_intelligent_practice_access(self, value):
        return self.context.setMemberProperties({'intelligent_practice_access': value})
    intelligent_practice_access = property(get_intelligent_practice_access,
                                           set_intelligent_practice_access)

    def get_trialuser(self):
        return self.context.getProperty('trialuser', '')
    def set_trialuser(self, value):
        return self.context.setMemberProperties({'trialuser': value})
    trialuser = property(get_trialuser, set_trialuser)

    def get_subscribe_to_maths_newsletter(self):
        return self.context.getProperty('subscribe_to_maths_newsletter', False)
    def set_subscribe_to_maths_newsletter(self, value):
        return self.context.setMemberProperties(
            {'subscribe_to_maths_newsletter': value})
    subscribe_to_maths_newsletter = property(
        get_subscribe_to_maths_newsletter, set_subscribe_to_maths_newsletter)

    def get_subscribe_to_science_newsletter(self):
        return self.context.getProperty('subscribe_to_science_newsletter', False)
    def set_subscribe_to_science_newsletter(self, value):
        return self.context.setMemberProperties(
            {'subscribe_to_science_newsletter': value})
    subscribe_to_science_newsletter = property(
        get_subscribe_to_science_newsletter, set_subscribe_to_science_newsletter)
