class Textfile():
    def __init__(self, filename, mode="r"):
        self.file = open(filename, mode)

    def close(self):
        self.file.close()

