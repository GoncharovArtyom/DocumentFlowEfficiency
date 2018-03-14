import re
import string as string_module
from functools import reduce


def analyzer(text, stemmer, stop_words):
    text = remove_punctuation(text)
    text = text.lower()
    words = text.split()
    words = fix_incorrect_word_and_tokenize(words)
    words = remove_stop_words(words, stop_words)
    stem_words = stemmer.stemWords(words)

    return stem_words

def dd_analyzer(text, stemmer):
    s = delete_spaces_and_new_lines(text)
    s = remove_punctuation(s)
    s = s.lower()
    s = remove_comments(s)
    str_list = s.split(" ")
    str_list = fix_incorrect_word_and_tokenize(str_list)
    str_list = stemmer.stemWords(str_list)
    str_list = remove_stop_words(str_list, stemmer)

    return str_list


def delete_spaces_and_new_lines(s):
    string = re.sub("\n+", " ", s)
    string = re.sub("\s(\s+)", " ", string)
    string = re.sub("^\s+", "", string)
    string = re.sub("\s+$", "", string)
    return string


def remove_punctuation(string):
    remove_dict = {ord(char):None for char in string_module.punctuation}
    return string.translate(remove_dict)


def fix_incorrect_word_and_tokenize(str_list):
    word_pattern = re.compile(r"^[а-я]+$|^[a-z]+$")
    number_pattern = re.compile(r"^[0-9]+$")
    result_str_list = reduce(lambda list_, x: list_ if (len(x) <= 2) else (
        list_ + [x] if (word_pattern.match(x) is not None) else (
            list_ + ['number'] if (number_pattern.match(x) is not None) else list_)), str_list, [])
    return result_str_list


def remove_stop_words(words, stop_words):
    reg_ex = re.compile("^" + "$|^".join(stop_words) + "$")
    return list(filter(lambda word: reg_ex.search(word) is None, words))

def remove_comments(s):
    pattern = re.compile("\^G|\^H")
    return pattern.sub('', s)
