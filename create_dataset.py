import argparse
import tempfile
import os

from data_mining.dataset import Dataset
from data_mining.dictionary.dictionary import Dictionary

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Dataset composing and creating tool.')
    parser.add_argument('dict_file', type=str, nargs=1, help='pronouncing dictionary file')
    parser.add_argument('freq_table', type=str, nargs=1, help='frequency csv table')
    parser.add_argument('sign_table', type=str, nargs=1, help='significance csv table')
    args = parser.parse_args()

    temp_file_path = os.path.join(tempfile.gettempdir(), 'temp_preprocessed_dict.list')

    print('Создание промежуточного файла словаря ...')
    Dictionary.preprocess(args.dict_file[0], temp_file_path)

    print('Генерирование датасета ...')
    Dataset.create(temp_file_path, args.freq_table[0], args.sign_table[0])
