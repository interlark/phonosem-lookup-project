from phonosem_lookup.sound_letter.extractor import SoundLetterExtractor
from phonosem_lookup.sound_letter.letter import SoundLetter
from phonosem_lookup.sound_letter.word import SoundWord
from phonosem_lookup.utils import read_csv
import re


class PhonosemanticAnalyzer:
    """
    Анализатор фоносемантической значимости слова.
    """

    FEATURE_TYPES = None  # список соответствующих фоносемантических шкал

    def __init__(self, sound_letters_frequency_file, sound_letters_significance_file):
        """
        Инициализация фоносемантического анализатора.
        :param sound_letters_frequency_file: Таблица частотности звукобукв.
        :param sound_letters_significance_file: Таблица значимости звукобукв.
        """
        self.sound_letter_significance_list = read_csv(sound_letters_significance_file)
        self.sound_letter_frequency_list = read_csv(sound_letters_frequency_file)
        self.sound_letter_extractor = SoundLetterExtractor()

        self.sound_letter_significance_dict = {}
        sound_positions_list = [(e.lower(), i) for i, e in enumerate(self.sound_letter_significance_list[0])
                                if re.match(r'[a-яё]\'?', e, re.IGNORECASE)]
        for sound_position in sound_positions_list:
            self.sound_letter_significance_dict[sound_position[0]] = list(
                [float(sound_letter_significance_line[sound_position[1]])
                 for n, sound_letter_significance_line in enumerate(self.sound_letter_significance_list) if n > 0])

        self.sound_letter_frequency_dict = {}
        sound_positions_list = [(e.lower(), i) for i, e in enumerate(self.sound_letter_frequency_list[0])
                                if re.match(r'[a-яё]\'?', e, re.IGNORECASE)]

        for sound_position in sound_positions_list:
            self.sound_letter_frequency_dict[sound_position[0]] = \
                float(self.sound_letter_frequency_list[1][sound_position[1]])

        if not self.FEATURE_TYPES:
            self.FEATURE_TYPES = list([sound_letter_significance_line[0] for n, sound_letter_significance_line in
                                       enumerate(self.sound_letter_significance_list) if n > 0])

    def get_feature_name(self, feature_index):
        """
        Получить название фоносемантической шкалы по её индексу.
        :param feature_index: индекс шкалы
        :return: название шкалы
        """
        return self.FEATURE_TYPES[feature_index]

    def analyze_word(self, word, stresses=None):
        """
        Фоносемантический анализ слова.
        :param word: слово
        :param stresses: список индексов ударных букв
        :return: список фоносемантических значений
        """

        sound_word = self.sound_letter_extractor.extract(word, stresses)
        return self.analyze_sound_word(sound_word)

    def analyze_sound_word(self, sound_word):
        """
        Фоносемантический анализ звуко-слова.
        :param sound_word: звуко-слово
        :return: список фоносемантических значений
        """
        significance_values = []
        frequencies_values = []
        stressed_letters_indexes = []
        
        if isinstance(sound_word, str):
            sound_word = SoundWord.from_sound_word(sound_word)
        
        for letter_index, sound_letter in enumerate(sound_word):
            if len(sound_letter) > 1 and sound_letter[0] in SoundLetter.VOWELS and sound_letter[1] == '\'':
                stressed_letters_indexes.append(letter_index)
                significance_values.append(self.sound_letter_significance_dict[sound_letter[:1]])
            else:
                significance_values.append(self.sound_letter_significance_dict[sound_letter])
            frequencies_values.append(self.sound_letter_frequency_dict[sound_letter])

        if not frequencies_values:
            # nothing to analyze
            return None

        frequencies_max_value = max(frequencies_values)
        frequencies_difference_coef_values = list([frequencies_max_value / value for value in frequencies_values])
        frequencies_difference_coef_values[0] *= 4

        for stressed_letter_index in stressed_letters_indexes:
            frequencies_difference_coef_values[stressed_letter_index] *= 2

        significance_difference_coef_values = []
        for n, significance_value in enumerate(significance_values):
            significance_difference_coef_values.append(list(map(
                lambda x: x * frequencies_difference_coef_values[n], significance_value)))

        frequencies_difference_coef_values_summary = sum(frequencies_difference_coef_values)
        result_values = []
        for n in range(len(self.sound_letter_significance_list) - 1):
            significance_letters_values_summary = sum([significance_letter_value[n] for significance_letter_value in
                                                       significance_difference_coef_values])
            result_values.append(significance_letters_values_summary / frequencies_difference_coef_values_summary)

        return result_values
