import molgenis

class MolgenisConnector:
    def __init__(self, url, username, password):
        self.session = molgenis.Session(url)
        self.session.login(username, password)

    def get_entity_by_id(self, entity, value):
        response = self.session.getById(entity=entity, id=value)
        response.pop('href', None)
        return response