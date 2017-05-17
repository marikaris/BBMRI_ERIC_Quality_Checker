import re
from idChecks import IdChecks


class CollectionIdChecks(IdChecks):
    def __init__(self, id, country):
        self.prefix = "bbmri-eric:ID:"
        self.country = country
        self.id = id
        self.country_acronyms = self.get_country_acronyms()

    def collection_correctly_placed(self):
        splitted_id = re.split(r"[_:]+", self.id)
        return splitted_id[2] == "collection"

    def get_messages(self):
        message = ''
        if not self.country_correct():
            message += "Countrycode incorrect: {} not in {}|".format(self.country_acronyms[self.country], self.id)
        if not self.prefix_ok():
            message += 'Invalid prefix: is should start with "{}" |'.format(self.prefix)
        if not self.collection_correctly_placed():
            message += 'Invalid prefix: "collection" should be placed after "bbmri-eric:ID:" |'
        return message[:-1]