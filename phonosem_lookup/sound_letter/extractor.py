from phonosem_lookup.sound_letter.word import SoundWord


class SoundLetterExtractor:
    """
    Модуль для извлечения звукобукв русского языка из слова.
    """

    @staticmethod
    def extract(input_word, stresses=None):
        """
        Метод извлечения звуко-слова (набора звуко-букв) из слова.
        :param input_word: Слово.
        :param stresses: Массив индексов ударных букв.
        :return: Звуко-слово.
        """
        input_word = input_word.lower()
        if stresses is None or not isinstance(stresses, list):
            raise ValueError('No stress found')
        return SoundWord(input_word, stresses)
