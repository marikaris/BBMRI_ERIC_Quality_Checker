from textfile import Textfile

class CountryCodeFileParser():
    def __init__(self, filename):
        self.codes = self.parse_file(filename)

    def parse_file(self, filename):
        country_code_file = Textfile(filename, 'r').file
        codes = {}
        for i, line in enumerate(country_code_file):
            if i != 0:
                vals = line.split(',')
                codes[vals[0]] = vals[1].strip('\n')
        return codes
