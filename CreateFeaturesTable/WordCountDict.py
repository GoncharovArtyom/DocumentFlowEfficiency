import pickle
import json as js
import Stemmer
import os
import re
import Analyzer
from math import *


class WordCountDict(object):
    def __init__(self):
        self._dict = {}
        self.Total = 0

    def AddOrInc(self, key):
        self._dict[key] = self._dict.setdefault(key, 0) + 1
        self.Total = self.Total + 1

    def AddOrIncList(self, listKeys):
        for i in range(len(listKeys)):
            self.AddOrInc(listKeys[i])

    def GetCount(self, key):
        return self._dict[key]

    def SaveToPkl(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL, fix_imports=False)

    def SaveToJson(self, path):
        f = open(path,'w')
        js.dump(self.__dict__,f,ensure_ascii=False)
        f.close()

    def CalcEntropy(self):
        if self.Total == 0:
            raise Exception

        entropy = 0
        values = self._dict.values()
        for val in values:
            p = val/self.Total
            entropy = entropy + p*log(p, 2)
        entropy = -entropy
        return entropy

    def DeleteMistakes(self):
        oldDict = self._dict
        self.Total = 0
        self._dict = {}

        for pair in oldDict.items():
            if pair[1] > 1:
                self.Total = self.Total + pair[1]
                self._dict[pair[0]] = pair[1]

    @staticmethod
    def LoadFromPkl(path):
        with open(path, 'rb') as f:
            obj = pickle.load(f, fix_imports=False)
            return obj

    @staticmethod
    def CreateDict(listDir, showProgress = False, printError = False, pathToData = "./data"):
        stemmer = Stemmer.Stemmer("russian")

        filePattern = re.compile(".*.txt$")
        wordCountDict = WordCountDict()
        error = []
        k = 0

        for i in range(len(listDir)):
            path = os.path.join(pathToData, listDir[i])
            listFiles = os.listdir(path)
            for j in range(len(listFiles)):
                result = re.match(filePattern, listFiles[j])
                if (result != None):
                    try:
                        f = open(os.path.join(path, result.string), 'r')
                        s = f.read()
                        f.close()
                        listString = Analyzer.Analyzer(s, stemmer)
                        wordCountDict.AddOrIncList(listString)
                        if (showProgress):
                            print(k)
                        k = k + 1
                    except UnicodeDecodeError:
                        error.append((listDir[i], listFiles[j]))
        if (showProgress):
            print("Done!")
        if (printError):
            print(error)
        return wordCountDict