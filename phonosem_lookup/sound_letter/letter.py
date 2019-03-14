class SoundLetter:
    """
    Класс для представления звуко-буквы.
    """

    VOWELS = 'аеёиоуыэюя'
    CONSONANTS = 'бвгджзйклмнпрстфхцчшщ'
    SONANT_DEAF_PAIRS = (
        ('б', 'п'),
        ('в', 'ф'),
        ('г', 'к'),
        ('д', 'т'),
        ('ж', 'ш'),
        ('з', 'с'),
    )

    ALWAYS_HARD_CONSONANTS = 'чщй'
    ALWAYS_SOFT_CONSONANTS = 'жшц'
    SONANT_PAIRED_CONSONANTS = [CONSONANT[0] for CONSONANT in SONANT_DEAF_PAIRS]
    DEAF_PAIRED_CONSONANTS = [CONSONANT[1] for CONSONANT in SONANT_DEAF_PAIRS]
    SOFT_SIGN = 'ь'
    HARD_SIGN = 'ъ'
    SIGN_LETTERS = SOFT_SIGN + HARD_SIGN
    TREAT_E = False                         # интерпретировать ё как е
    SUPPRESS_CONSONANTS_IN_A_ROW = False    # вывод одной согласной вместно нескольких подряд
    SUPPRESS_VOWELS_IN_A_ROW = False        # вывод одной гласной вместно нескольких подряд
    ALWAYS_SOFT_CONSONANTS_SIGN = False     # проставлять апостроф для всегда мягких согласных ч, щ, й

    def __init__(self, letter, is_stressed=False):
        if is_stressed and letter not in SoundLetter.VOWELS:
            raise Exception('Согласная буква не может быть ударной')
        self.letter = letter
        self.is_stressed = is_stressed
        self.is_muted = False
        self.previous = None
        self.next = None

    def _has_apostrophe_sign(self, sound_letter):
        return len(sound_letter) != 0 and sound_letter[-1] == '\''

    def get_sound_letter(self):
        if SoundLetter.SUPPRESS_CONSONANTS_IN_A_ROW:
            if self.letter in SoundLetter.CONSONANTS and \
                    self.next is not None and self.next.letter == self.letter:
                self.is_muted = True

        if SoundLetter.SUPPRESS_VOWELS_IN_A_ROW:
            if self.letter in SoundLetter.VOWELS and \
                    self.next is not None and self.next.letter == self.letter:
                self.is_muted = True

        set_apostrophe_sign = False

        if self.letter in SoundLetter.SIGN_LETTERS:
            self.is_muted = True

        if SoundLetter.TREAT_E and self.letter == 'ё':
            self.letter = 'е'

        if self.letter in SoundLetter.CONSONANTS:
            # смягчение знаком ь
            if self.next is not None and self.next.letter == SoundLetter.SOFT_SIGN:
                set_apostrophe_sign = True

            # твёрдые согласные перед мягкими смягчаються
            # TODO: исключения
            if self.next is not None and self.next.letter in SoundLetter.CONSONANTS \
                    and self._has_apostrophe_sign(self.next.get_sound_letter()):
                set_apostrophe_sign = True

            # согласные смягчаются, если сразу за ними следуют гласные буквы е, ё, и, ю, я
            # TODO: исключения
            if self.next is not None and self.next.letter in ['е', 'ё', 'и', 'ю', 'я']:
                set_apostrophe_sign = True

        if self.letter in SoundLetter.VOWELS:
            if self.is_stressed:
                set_apostrophe_sign = True

        if self.letter in SoundLetter.ALWAYS_HARD_CONSONANTS:
            set_apostrophe_sign = False

        if self.letter in SoundLetter.ALWAYS_SOFT_CONSONANTS:
            if SoundLetter.ALWAYS_SOFT_CONSONANTS_SIGN:
                set_apostrophe_sign = True
            else:
                set_apostrophe_sign = False

        sound_letter = self.letter + ('\'' if set_apostrophe_sign else '')
        return sound_letter if not self.is_muted else ''
