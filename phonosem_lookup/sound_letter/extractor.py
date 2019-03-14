from phonosem_lookup.sound_letter.word import SoundWord


class SoundLetterExtractor:
    """
    Модуль для извлечения звукобукв русского языка из слова.
    """

    @staticmethod
    def extract(input_word, stresses=None):
        """
        Метод извлечения звуко-слова (набора звуко-букв) из слова.
        :param input_word: слово
        :param stresses: массив индексов ударных букв
        :return: звуко-слово
        """
        input_word = input_word.lower()
        if stresses is None or not isinstance(stresses, list):
            raise ValueError('No stress found')
        return SoundWord(input_word, stresses)
