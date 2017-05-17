import re
from idChecks import IdChecks

class NetworkIdChecks(IdChecks):
    def __init__(self, id):
        self.prefix = 'bbmri-eric_bbnetID:'
        self.id = id
        self.country_acronyms = list(self.get_country_acronyms().values())
        self.country_acronyms.append('EU')

    def country_correct(self):
        splitted_id = re.split(r"[_:]+", self.id)
        return splitted_id[2] in self.country_acronyms

    def get_messages(self):
        message = ''
        if not self.prefix_ok():
            message += 'Invalid prefix: is should start with "{}" |'.format(self.prefix)
        if not self.country_correct():
            message += "Countrycode incorrect in: "+ self.id
        return message[:-1]