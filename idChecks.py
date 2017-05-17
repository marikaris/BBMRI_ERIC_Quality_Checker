import re
from countryCodeParser import CountryCodeFileParser

class IdChecks:
    def __init__(self, id, country):
        self.id = id
        self.prefix = "bbmri-eric:ID:"
        self.country = country
        self.country_acronyms = self.get_country_acronyms()

    def prefix_ok(self):
        return self.id.startswith(self.prefix)

    def country_correct(self):
        splitted_id = re.split(r"[_:]+", self.id)
        return self.country_acronyms[self.country] in splitted_id

    def get_country_acronyms(self):
        return CountryCodeFileParser('country_codes.csv').codes

    def get_messages(self):
        message = ''
        if not self.country_correct():
            message += "Countrycode incorrect: {} not in {}|".format(self.country_acronyms[self.country], self.id)
        if not self.prefix_ok():
            message += 'Invalid prefix: is should start with "{}" |'.format(self.prefix)
        return message[:-1]