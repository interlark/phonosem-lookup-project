#!/usr/bin/env python3

import argparse
import re

from keras.models import load_model
import numpy as np

from phonosem_lookup.phonosem.analyzer import PhonosemanticAnalyzer
from phonosem_lookup.sound_letter.word import SoundWord

PHONOSEM_VALUES_LEN = 25
PHONOSEM_VALUES_SCALE = 6
SOUND_WORD_SET = ' аеёиоуыэюяа\'е\'ё\'и\'о\'у\'ы\'э\'ю\'я\'бб\'вв\'гг\'дд\'жзз\'йкк\'лл\'мм\'нн\'пп\'рр\'сс\'тт\'фф\'хх\'цчшщ'
SOUND_WORD_DIC = {k: i for i, k in enumerate(re.findall(r'[\sа-яё]\'?', SOUND_WORD_SET))}


def sound_char_tensor_to_sound_char(sound_char_tensor):
    sound_char_idx = np.argmax(sound_char_tensor)
    for c, i in SOUND_WORD_DIC.items():
        if i == sound_char_idx:
            return c


def make_phonosem(feature_idx, direction):
    ret = np.random.rand(PHONOSEM_VALUES_LEN)
    ret[feature_idx] = 0.01 if direction == 'LEFT' else 0.99
    return np.array([ret])


def get_sound_word(sound_chars_tensor):
    sound_word = ''
    for i in range(len(sound_chars_tensor)):
        sound_word += sound_char_tensor_to_sound_char(sound_chars_tensor[i])
    return sound_word


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple phonosemantic word lookup based on machine learning.')
    parser.add_argument('--skip-inappropriate', dest='skip', action='store_true', help='skip inappropriate words')
    parser.add_argument('freq_table', type=str, nargs=1, help='frequency csv table')
    parser.add_argument('sign_table', type=str, nargs=1, help='significance csv table')
    parser.add_argument('model', type=str, nargs=1, help='model file')
    parser.add_argument('feature_idx', type=int, help='feature index')
    parser.add_argument('direction', choices=['LEFT', 'RIGHT'], help='feature direction')
    args = parser.parse_args()
    model_file = args.model[0]
    sound_letters_frequency_file = args.freq_table[0]
    sound_letters_significance_file = args.sign_table[0]
    direction = args.direction
    feature_idx = args.feature_idx

    model = load_model(model_file)
    phonosem_analyzer = PhonosemanticAnalyzer(sound_letters_frequency_file, sound_letters_significance_file)

    print('Выбранная шкала:', phonosem_analyzer.FEATURE_TYPES[feature_idx])
    print('Выбранное направление:', phonosem_analyzer.FEATURE_TYPES[feature_idx].split('-')[0 if direction == 'LEFT' else 1])

    try:
        while True:
            while True:
                phonetics = make_phonosem(feature_idx, direction)
                tensor_sound_word = model.predict(phonetics)
                sound_word = get_sound_word(tensor_sound_word)
                predicted_phonosemantic_values = phonosem_analyzer.analyze_sound_word(SoundWord.from_sound_word(sound_word))
                if not args.skip:
                    break
                elif direction == 'LEFT':
                    if predicted_phonosemantic_values[feature_idx] <= 2.5:
                        break
                else:
                    if predicted_phonosemantic_values[feature_idx] >= 3.5:
                        break
            print('Сгенерированное звуко-слово:', sound_word)
            print('Полученное значение признака:', predicted_phonosemantic_values[feature_idx])
            input()
    except KeyboardInterrupt:
        pass
