from idChecks import IdChecks

class PersonIdChecks(IdChecks):
    def __init__(self, id, country):
        self.prefix = 'bbmri-eric:contactID:'
        self.country = country
        self.id = id
        self.country_acronyms = self.get_country_acronyms()

    def get_messages(self):
        message = ''
        if not self.country_correct():
            message += "Countrycode incorrect: {} not in {}|".format(self.country_acronyms[self.country], self.id)
        if not self.prefix_ok():
            message += 'Invalid prefix: is should start with "{}" |'.format(self.prefix)
        return message[:-1]