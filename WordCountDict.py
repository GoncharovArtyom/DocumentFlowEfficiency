import Stemmer
import json as js
import os
import pickle
import re
from math import *

import Analyzer


class WordCountDict(object):
    def __init__(self):
        self._dict = {}
        self.Total = 0

    def add_or_inc(self, key):
        self._dict[key] = self._dict.setdefault(key, 0) + 1
        self.Total = self.Total + 1

    def add_or_inc_list(self, list_keys):
        for i in range(len(list_keys)):
            self.add_or_inc(list_keys[i])

    def get_count(self, key):
        return self._dict[key]

    def save_to_pkl(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL, fix_imports=False)

    def save_to_json(self, path):
        f = open(path, 'w')
        js.dump(self.__dict__, f, ensure_ascii=False)
        f.close()

    def calc_entropy(self):
        if self.Total == 0:
            raise Exception

        entropy = 0
        values = self._dict.values()
        for val in values:
            p = val / self.Total
            entropy = entropy + p * log(p, 2)
        entropy = -entropy
        return entropy

    def max_entropy(self):
        if self.Total == 0:
            raise Exception

        entropy = 0
        num_dictinct_words = self.num_distinct_words
        for i in range(num_dictinct_words):
            p = 1/num_dictinct_words
            entropy = entropy + p * log(p, 2)
        entropy = -entropy
        return entropy

    def calc_zipf_entropy(self):
        if self.Total == 0:
            raise Exception

        ZIPF_CONSTANT = 0.07
        entropy = 0
        num_dictinct_words = self.num_distinct_words
        for i in range(num_dictinct_words):
            p = ZIPF_CONSTANT / (i+1)
            entropy = entropy + p * log(p, 2)
        entropy = -entropy
        return entropy

    @property
    def num_distinct_words(self):
        return len(self._dict.keys())

    def delete_words_with_freq_lower_than(self, low_frequency_bound):
        if (type(low_frequency_bound) == type(float)):
            low_frequency_bound = round(self.Total * low_frequency_bound)

        old_dict = self._dict
        self.Total = 0
        self._dict = {}

        for pair in old_dict.items():
            if pair[1] >= low_frequency_bound:
                self.Total = self.Total + pair[1]
                self._dict[pair[0]] = pair[1]

    def delete_words_with_freq_greater_than(self, high_frequency_bound):
        if (type(high_frequency_bound) == type(float)):
            high_frequency_bound = round(self.Total * high_frequency_bound)

        old_dict = self._dict
        self.Total = 0
        self._dict = {}

        for pair in old_dict.items():
            if pair[1] > high_frequency_bound:
                self.Total = self.Total + pair[1]
                self._dict[pair[0]] = pair[1]

    @staticmethod
    def load_from_pkl(path):
        with open(path, 'rb') as f:
            obj = pickle.load(f, fix_imports=False)
            return obj

    @staticmethod
    def create_dict(list_dir, analyzer, show_progress=False, print_error=False,
                    path_to_data="./data"):
        stemmer = Stemmer.Stemmer("russian")

        file_pattern = re.compile(".*.txt$")
        word_count_dict = WordCountDict()
        error = []
        k = 0

        for i in range(len(list_dir)):
            path = os.path.join(path_to_data, list_dir[i])
            list_files = os.listdir(path)
            for j in range(len(list_files)):
                result = re.match(file_pattern, list_files[j])
                if result is not None:
                    try:
                        f = open(os.path.join(path, result.string), 'r')
                        s = f.read()
                        f.close()
                        list_string = analyzer(s, stemmer)
                        word_count_dict.add_or_inc_list(list_string)
                        if show_progress:
                            print(k)
                        k = k + 1
                    except UnicodeDecodeError:
                        error.append((list_dir[i], list_files[j]))
        if show_progress:
            print("Done!")
        if print_error:
            print(error)
        return word_count_dict
