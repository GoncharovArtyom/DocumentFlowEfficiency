import re
from functools import reduce


def analyzer(text, stemmer):
    s = delete_spaces_and_new_lines(text)
    s = remove_punctuation(s)
    s = s.lower()
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


def remove_punctuation(s):
    string = re.sub("\s\W", " ", s)
    string = re.sub("\W\s", " ", string)
    string = re.sub("\s\W\s", " ", string)
    string = re.sub("_", " ", string)
    return string


def fix_incorrect_word_and_tokenize(str_list):
    russian_word_pattern = re.compile(r"^[а-я]+$")
    number_pattern = re.compile(r"^[0-9]+$")
    result_str_list = reduce(lambda list_, x: list_ if (len(x) <= 2) else (
        list_ + [x] if (russian_word_pattern.match(x) is not None) else (
            list_ + ['number'] if (number_pattern.match(x) is not None) else list_)), str_list, [])
    return result_str_list


def remove_stop_words(str_list, stemmer):
    stop_words_list = ["быть", "вот", "еще", "как", "нет", "они", "сказать", "только", "этот",
                       "большой",
                       "все", "говорить", "для", "который", "него", "них", "один", "оно", "ото",
                       "свой",
                       "тот", "что", "весь", "всей", "год", "знать", "мочь", "наш", "нее", "она",
                       "оный",
                       "себя", "такой", "это"]
    stop_words_list = stemmer.stemWords(stop_words_list)
    stop_words_re = re.compile("^" + "$|^".join(stop_words_list) + "$")

    return list(filter(lambda item: stop_words_re.search(item) is None, str_list))
