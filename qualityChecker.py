from molgenisConnector import MolgenisConnector
from logwriter import LogWriter
from collectionIdChecks import CollectionIdChecks
from idChecks import IdChecks
from networkIdChecks import NetworkIdChecks
from personIdChecks import PersonIdChecks
from configParser import ConfigParser

import re

class QualityChecker():
    """NAME: QualityChecker
    PURPOSE: Checks if the values in the MOLGENIS database of BBMRI-ERIC are filled in correctly
    OUT: logs.txt - file with all errors in the database"""
    def __init__(self, connnection):
        self.connection = connnection
        self.collection_data = self.get_collection_data()
        self.biobank_data = self.get_biobank_data()
        self.network_data = self.get_network_data()
        self.person_data = self.get_person_data()
        self.logs = LogWriter("logs.txt")
        self.logs.reset()

    def get_network_data(self):
        """NAME: get_network_data
        PURPOSE: retrieves network data from molgenis
        OUT: dictionary with data inside networks"""
        return self.connection.session.get("eu_bbmri_eric_networks", num=10000)

    def get_person_data(self):
        """NAME: get_person_data
        PURPOSE: retrieves person data from molgenis
        OUT: dictionary with data inside persons"""
        return self.connection.session.get("eu_bbmri_eric_persons", num=10000)

    def get_collection_data(self):
        """NAME: get_collection_data
        PURPOSE: retrieves collections data from molgenis
        OUT: dictionary with data inside collections"""
        return self.connection.session.get("eu_bbmri_eric_collections", num=10000)

    def get_biobank_data(self):
        """NAME: get_biobank_data
        PURPOSE: retrieves biobank data from molgenis
        OUT: dictionary with data inside biobanks"""
        return self.connection.session.get("eu_bbmri_eric_biobanks", num=10000)

    def is_valid_collection_id(self, id, country):
        """NAME: is_valid_collection_id
        PURPOSE: checks if collection id is valid
        IN: id - the id to check
            country - the country specified for the collection
        OUT: writes to log file when invalid"""
        collection_qc = CollectionIdChecks(id, country)
        msg = collection_qc.get_messages()
        if len(msg) > 0:
            self.logs.write(id, 'collection_id', collection_qc.get_messages(), 'CRITICAL', 'COLLECTION HAS INVALID ID')

    def is_valid_biobank_id(self, id, country):
        """NAME: is_valid_biobank_id
        PURPOSE: checks if biobank id is valid
        IN: id - the id to check
            country - the country specified for the biobank
        OUT: writes to log file when invalid"""
        biobank_qc = IdChecks(id, country)
        msg = biobank_qc.get_messages()
        if len(msg) > 0:
            self.logs.write(id, 'biobank_id', biobank_qc.get_messages(), 'CRITICAL', 'BIOBANK HAS INVALID ID')

    def is_valid_person_id(self, id, country):
        """NAME: is_valid_person_id
        PURPOSE: checks if person id is valid
        IN: id - the id to check
            country - the country specified for the person
        OUT: writes to log file when invalid"""
        person_qc = PersonIdChecks(id, country)
        msg = person_qc.get_messages()
        if len(msg) > 0:
            self.logs.write(id, 'person_id', person_qc.get_messages(), 'CRITICAL', 'PERSON HAS INVALID ID')

    def is_valid_network_id(self, id):
        """NAME: is_valid_network_id
        PURPOSE: checks if network id is valid
        IN: id - the id to check
            country - the country specified for the network
        OUT: writes to log file when invalid"""
        network_qc = NetworkIdChecks(id)
        msg = network_qc.get_messages()
        if self.not_empty(msg):
            self.logs.write(id, 'network_id', network_qc.get_messages(), 'CRITICAL', 'NETWORK HAS INVALID ID')
        else:
            print('passed: ', id)

    def not_empty(self, value):
        """NAME: not_empty
        PURPOSE: checks if a valus is not empty or empty like (NA / N/A)
        IN: value - the value that needs to be checked for emptyness
        OUT: Boolean; TRUE if value is of length 0 or 'NA' or 'N/A', else FALSE"""
        return len(value) > 0 and value != 'NA' and value != 'N/A'

    def check_name(self, id, name, type):
        """NAME: check_name
        PURPOSE: checks if the name is not empty
        IN:     id - the id of the row that has this name
                name - the name to check
                type - can be collection, biobank, network
        OUT: writes to log file when invalid"""
        if not self.not_empty(name):
            self.logs.write(id, type+'_name', 'Name not specified', 'CRITICAL', type.upper()+' MISSING NAME')

    def check_description(self, row, type):
        if 'description' in row:
            description = row['description']
            stripped_description = re.sub(r'collection|samples', '', description, flags=re.IGNORECASE)
            stripped_description = stripped_description.strip('.')
            stripped_description = stripped_description.strip(' ')
            if len(stripped_description) < 30:
                self.logs.write(row['id'], type+'_description', 'WARNING: Description length < 30: '+description, 'WARNING', type.upper()+' HAS SHORT DESCRIPTION')
        else:
            self.logs.write(row['id'], type+'_description', 'Description empty', 'CRITICAL', type.upper()+ ' MISSING DESCRIPTION')

    def check_contact(self, id, contact, type):
        if not len(contact) == 1:
            self.logs.write(id, type+'_contact', 'More than one contact: '+ str(len(contact)), 'CRITICAL', type.upper()+' HAS MORE THAN 1 CONTACT')

    def is_wild_card_diagnosis(self, list, id):
        for diagnosis in list:
            if '*' in diagnosis['id'] or '-' in diagnosis['id']:
                self.logs.write(id, 'collection_diagnosis', 'WARNING: Diagnosis contains wildcard: '+diagnosis['id'], 'WARNING', 'COLLECTION DIAGNOSIS CONTAINS WILDCARD')

    def check_biobank_head(self, row):
        id = row['id']
        if not 'head_firstname' in row:
            self.logs.write(id, 'biobank_head_firstname', 'Head firstname not defined', 'CRITICAL', 'BIOBANK MISSING HEAD FIRSTNAME')
        if not 'head_lastname' in row:
            self.logs.write(id, 'biobank_head_lastname', 'Head lastname not defined', 'CRITICAL', 'BIOBANK MISSING LAST FIRSTNAME')

    def check_collaboration(self, row, type):
        id = row['id']
        if not 'collaboration_commercial' in row:
            self.logs.write(id, type+'_collaboration', 'Collaboration commercial not specified', 'CRITICAL', type.upper()+' MISSING COLLABORATION COMMERCIAL')
        if not 'collaboration_non_for_profit' in row:
            self.logs.write(id, type+'collection_collaboration', 'Collaboration non for profit not specified', 'CRITICAL', type.upper()+' MISSING COLLABORATION NON FOR PROFIT')

    def check_sample_image_data(self, row):
        id = row['id']
        if ('image_access_description' in row or 'image_access_fee' in row) and len(row['image_dataset_type']) == 0:
            self.logs.write(id, 'collection_data', 'Image access description/fee not specified while image dataset type is', 'CRITICAL', 'COLLECTION MISSING IMAGE ACCESS DESCRIPTION/FEE')
        elif 'image_access_description' not in row and 'image_access_fee' not in row and len(row['image_dataset_type']) > 0:
            self.logs.write(id, 'collection_data', 'Image dataset type not specified while image access description/fee is', 'CRITICAL', 'COLLECTION MISSING IMAGE DATASET TYPE')
        if ('sample_access_description' in row or 'sample_access_fee' in row) and len(row['materials']) == 0:
            self.logs.write(id, 'collection_data', 'Materials not specified while sample access description/fee is', 'CRITICAL', 'COLLECTION MISSING SAMPLE DATASET TYPE')
        elif 'sample_access_description' not in row and 'sample_access_fee' not in row and len(row['materials']) > 0:
            self.logs.write(id, 'collection_data', 'Sample access description/fee not specified while materials is', 'CRITICAL', 'COLLECTION MISSING SAMPLE ACCESS DESCRIPTION/FEE')

    def check_geolocation(self, row, type):
        id = row['id']
        if 'latitude' not in row or 'longitude' not in row:
            self.logs.write(id, type+'_geolocation', 'latitude/longitude not defined', 'WARNING', type.upper()+' MISSING LATITUDE/LONGITUDE')

    def check_network_juridical_person(self, row):
        id = row['id']
        if 'juridical_person' not in row:
            self.logs.write(id, 'network_juridical_person', 'Juridical person not defined', 'CRITICAL', 'NETWORK MISSING JURIDICAL PERSON')

    def check_person_phonenumber(self, row):
        id = row['id']
        if 'phone' in row:
            phone = row['phone']
            if not re.match(r'^\+(?:[0-9]??){6,14}[0-9]$', phone):
                self.logs.write(id, 'network_juridical_person', 'Phone number formatted incorrect, not matching pattern: ^\+(?:[0-9]??){6,14}[0-9]$', 'CRITICAL', 'PERSON PHONE NUMBER FORMATTED INCORRECT')
        else:
            self.logs.write(id, 'person_phone', 'Phone number not defined', 'WARNING', 'PERSON MISSING PHONE NUMBER')

    def check_person_data(self):
        for row in self.person_data:
            id = row['id']
            country = row["country"]['name']
            self.is_valid_person_id(id, country)
            self.check_person_phonenumber(row)

    def check_network_data(self):
        for row in self.network_data:
            id = row['id']
            self.is_valid_network_id(id)
            self.check_geolocation(row, 'network')
            self.check_name(id, row['name'], 'network')
            self.check_description(row, 'network')
            self.check_network_juridical_person(row)
            self.check_contact(id, row['contact'], 'network')
            self.check_collaboration(row, 'network')


    def check_biobank_data(self):
        for row in self.biobank_data:
            id = row['id']
            country = row["country"]['name']
            self.is_valid_biobank_id(id, country)
            self.check_geolocation(row, 'biobank')
            self.check_name(id, row['name'], 'biobank')
            self.check_description(row, 'biobank')
            self.check_biobank_head(row)
            self.check_contact(id, row['contact'], 'biobank')
            self.check_collaboration(row, 'biobank')

    def check_collection_data(self):
        # Check collection data
        for row in self.collection_data:
            id = row['id']
            country = row["country"]['name']
            # Check collection id
            self.is_valid_collection_id(id, country)
            self.check_name(id, row['name'], 'collection')
            self.check_description(row, 'collection')
            self.check_contact(id, row['contact'], 'collection')
            self.is_wild_card_diagnosis(row['diagnosis_available'], id)
            self.check_collaboration(row, 'collection')
            self.check_sample_image_data(row)


def main():
    config = ConfigParser().config
    molgenis_connector = MolgenisConnector(config['url'], config['account'], config['password'])
    qc = QualityChecker(molgenis_connector)
    qc.check_collection_data()
    qc.check_biobank_data()
    qc.check_network_data()
    qc.check_person_data()
    molgenis_connector.logs.close()

if __name__ == "__main__":
    main()
