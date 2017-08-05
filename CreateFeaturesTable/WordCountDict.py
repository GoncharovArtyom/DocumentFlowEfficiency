import pickle

class WordCountDict(object):
    def __init__(self):
        self.__dict = {}
        self.Total = 0

    def AddOrInc(self, key):
        self.__dict[key] = self.__dict.setdefault(key, 0) + 1
        self.Total = self.Total + 1

    def AddOrIncList(self, listKeys):
        for i in range(len(listKeys)):
            self.AddOrInc(listKeys[i])

    def GetCount(self, key):
        return self.__dict[key]

    def Save(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def LoadFromPkl(path):
        with open(path, 'rb') as f:
            obj = pickle.load(f)
            return obj