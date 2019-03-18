import os
import time
import requests
import re
import progressbar
from datetime import datetime


class Dictionary:
    """
    Класс для работы с данными из орфоэпического словаря русского языка.
    """

    @staticmethod
    def preprocess(source_file, destination_file):
        """
        Метод для парсинга орфоэпического словаря и формирование промежуточного файла формата:
        <cлово>\t<индекс ударной буквы [,индекс ударной буквы]>\t<индекс ударной буквы [,индекс ударной буквы]>
        :param source_file: путь до орфоэпического словаря.
        :param destination_file: путь для формируемого файла.
        :return: None
        """

        with open(source_file, 'r', encoding='utf-8') as dict_file:
            with open(destination_file, 'w', encoding='utf-8') as list_file:
                for line in dict_file:
                    for word in line.split('#')[1].split(','):
                        if word == '-':
                            continue
                        word = word.strip()
                        pos = -1
                        clean_word = ''
                        primary = []  # ', ё
                        secondary = []  # `
                        for ch in word:
                            if ch in ('\'', '`'):
                                if ch == '`':
                                    secondary.append(pos)
                                else:
                                    primary.append(pos)
                                continue
                            clean_word += ch
                            pos += 1
                            if ch == "ё":
                                primary.append(pos)
                        if len(primary) > 0:
                            list_file.write(
                                clean_word + '\t' + ','.join([str(a) for a in primary]) + '\t' +
                                ','.join([str(a) for a in secondary]) + '\n')

    @staticmethod
    def load_word_stress_dict(source_file):
        """
        Метод загрузки промежуточного файла словаря.
        :param source_file: путь до промежуточного файла словаря
        :return: словарь типа слово -> множество ударений
        """
        stress_dict = {}
        with open(source_file, 'r', encoding='utf-8') as list_file:
            for line in list_file:
                word, primary, secondary = line.split('\t')
                primary = primary.strip()
                secondary = secondary.strip()
                stresses = [int(acc) for acc in primary.strip().split(',')]
                if len(secondary) > 0:
                    stresses += [int(acc) for acc in secondary.strip().split(',')]
                if word not in stress_dict:
                    stress_dict[word] = set(stresses)
                else:
                    stress_dict[word].update(stresses)

        return stress_dict  # dict(word, list(stress))
