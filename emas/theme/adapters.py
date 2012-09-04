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

    def get_ua_device(self):
        return self._getProperty('ua_device')
    def set_ua_device(self, value):
        return self.context.setMemberProperties({'ua_device': value})
    ua_device = property(get_ua_device, set_ua_device)

    def get_ua_pixels(self):
        return self._getProperty('ua_pixels')
    def set_ua_pixels(self, value):
        return self.context.setMemberProperties({'ua_pixels': value})
    ua_pixels = property(get_ua_pixels, set_ua_pixels)

    def get_mxitcontact(self):
        return self._getProperty('mxitcontact')
    def set_mxitcontact(self, value):
        return self.context.setMemberProperties({'mxitcontact': value})
    mxitcontact = property(get_mxitcontact, set_mxitcontact)

    def get_country(self):
        return self._getProperty('country')
    def set_country(self, value):
        return self.context.setMemberProperties({'country': value})
    country = property(get_country, set_country)

    def get_birthdate(self):
        return self._getProperty('birthdate')
    def set_birthdate(self, value):
        return self.context.setMemberProperties({'birthdate': value})
    birthdate = property(get_birthdate, set_birthdate)

    def get_gender(self):
        return self._getProperty('gender')
    def set_gender(self, value):
        return self.context.setMemberProperties({'gender': value})
    gender = property(get_gender, set_gender)


