import re
from idChecks import IdChecks


class CollectionIdChecks(IdChecks):
    def __init__(self, id, country, biobankId):
        self.prefix = "bbmri-eric:ID:"
        self.country = country
        self.id = id
        self.country_acronyms = self.get_country_acronyms()
        self.biobankId = biobankId

    def collection_correctly_placed(self):
        splitted_id = re.split(r"[_:]+", self.id)
        if splitted_id.index("collection") > 3:
            return True
        else:
            return False

    def is_valid_biobank(self):
        splitted_id = self.id.split(":collection:")
        return splitted_id[0] == self.biobankId

    def get_messages(self):
        message = ''
        if not self.country_correct():
            message += "Countrycode incorrect: {} not in {}|".format(self.country_acronyms[self.country], self.id)
        if not self.prefix_ok():
            message += 'Invalid prefix: is should start with "{}" |'.format(self.prefix)
        if not self.collection_correctly_placed():
            message += 'Invalid prefix: Collection id should be constructed from biobankID prefix + :collection: + local collection ID string |'
        else:
            if not self.is_valid_biobank():
                message += 'Invalid prefix: biobankID not present in biobank table |'
        return message[:-1]