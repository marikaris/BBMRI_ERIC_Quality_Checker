from textfile import Textfile

class LogWriter():
    def __init__(self, name):
        self.name = name
        self.logfile = Textfile(name, 'a').file

    def write(self, id, type, problem, status, summary):
        self.logfile.write(id+'\t'+type+'\t'+problem+'\t'+status+'\t'+summary+'\n')

    def reset(self):
        self.logfile.close()
        self.logfile = Textfile(self.name, 'w').file
        self.logfile.write('id\ttype\tproblem\tstatus\tsummary\n')