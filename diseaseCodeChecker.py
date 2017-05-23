import re


class DiseaseCodeChecker():
    def __init__(self):
        self.warningCodes = ['ORDO', 'orphanet', 'urn:miriam:icd:*', 'urn:miriam:icd:A04*']
        self.errorCodes = ['NA', 'OMIM', 'TRUE', 'urn:miriam:icd:01', 'urn:miriam:icd:02', 'urn:miriam:icd:03',
                           'urn:miriam:icd:04', 'urn:miriam:icd:05', 'urn:miriam:icd:06', 'urn:miriam:icd:07',
                           'urn:miriam:icd:08', 'urn:miriam:icd:09', 'urn:miriam:icd:10', 'urn:miriam:icd:11',
                           'urn:miriam:icd:12', 'urn:miriam:icd:13', 'urn:miriam:icd:14', 'urn:miriam:icd:15',
                           'urn:miriam:icd:16', 'urn:miriam:icd:17', 'urn:miriam:icd:18', 'urn:miriam:icd:19',
                           'urn:miriam:icd:20', 'urn:miriam:icd:21', 'urn:miriam:icd:22', 'urn:miriam:icd:A0']

    def is_valid_code(self, code, list):
        if code in list:
            return False
        else:
            return True

    def has_wildcard(self, code):
        pattern = r"(urn:miriam:icd:[A-Z]{1}\d{1,2})(\*)"
        if re.match(pattern, code):
            return True
        else:
            return False

    def check_code(self, code):
        log = []
        if not self.is_valid_code(code, self.warningCodes):
            log.append('WARNING: Diagnosis contains wildcard: ' + code)
            log.append('WARNING')
            log.append('COLLECTION DIAGNOSIS CONTAINS WILDCARD')
            return log
        elif not self.is_valid_code(code, self.errorCodes):
            log.append('Diagnosis code not valid: ' + code)
            log.append('CRITICAL')
            log.append('COLLECTION DIAGNOSIS CODE NOT VALID')
            return log
        elif self.has_wildcard(code):
            log.append('WARNING: Diagnosis contains wildcard: ' + code)
            log.append('WARNING')
            log.append('COLLECTION DIAGNOSIS CONTAINS WILDCARD')
            return log
