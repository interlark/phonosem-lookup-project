from phonosem_lookup.sound_letter.letter import SoundLetter
import re


class SoundWord:
    """
    Класс для представления звуко-слова.
    """
    def __init__(self, word, stresses):
        self.word = word
        self.stresses = stresses

    def as_sound_word(self):
        letters_chain = []
        for n, current_letter in enumerate(self.word):
            letter = SoundLetter(current_letter, is_stressed=n in self.stresses)
            letters_chain.append(letter)

        letters_chain = [letter for letter in letters_chain if re.search(r'[а-яё]', letter.letter)]

        for n in range(len(letters_chain)):
            if n + 1 < len(letters_chain):
                letters_chain[n].next = letters_chain[n + 1]
            if n > 0:
                letters_chain[n].previous = letters_chain[n - 1]

        return ''.join(letter.get_sound_letter() for letter in letters_chain)

    def __iter__(self):
        pattern = re.compile(r'[а-яё]\'?')
        word = self.as_sound_word() if not self.sound_word else self.sound_word
        for match in re.finditer(pattern, word):
            yield match.group()

    def __str__(self):
        return self.as_sound_word()

    def __repr__(self):
        word = self.as_sound_word()
        return '<{class_name} word={word} value={sound_word}>'.format(
            class_name=self.__class__.__name__,
            word=self.word,
            sound_word=word)

    @classmethod
    def from_sound_word(cls, sound_word):
        ret = cls(None, None)
        ret.sound_word = sound_word
        return ret
