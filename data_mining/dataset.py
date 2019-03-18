import MySQLdb
import multiprocessing
import pymorphy2
from functools import partial
from progressbar import ProgressBar

from data_mining.dictionary.dictionary import Dictionary
from phonosem_lookup.phonosem.analyzer import PhonosemanticAnalyzer
from phonosem_lookup.sound_letter.word import SoundWord

from settings import DB_HOST, DB_USER, DB_PASS, DB_NAME


class Dataset:
    """
    Класс для подготовки датасета в MySQL.
    Оценочно 2500000 слов.
    """

    POOL_SIZE = 4  # Размер пула процессов создания датасета

    @staticmethod
    def create(dictionary_preprocessed_file, sound_letters_frequency_file, sound_letters_significance_file):
        """
        Определение части речи, звуко-слова и подсчет фоносемантической значимости слов орфоэпического словаря.
        :param dictionary_preprocessed_file: Путь до промежуточного файла орфоэпического словаря.
        :param sound_letters_frequency_file: Путь до таблицы частотности звукобукв.
        :param sound_letters_significance_file: Путь до таблицы значимости звукобукв.
        :return: Датасет в БД
        """
        dic = Dictionary.load_word_stress_dict(dictionary_preprocessed_file)

        # for word in dic.keys():
        #     stresses = list(dic[word])
        #     # print('word \'%s\' has stresses=%s' % (word, stresses))

        phonosem_analyzer = PhonosemanticAnalyzer(sound_letters_frequency_file, sound_letters_significance_file)
        morph_analyzer = pymorphy2.MorphAnalyzer()

        pbar = ProgressBar(maxval=len(dic), redirect_stdout=True).start()
        prc_func = partial(Dataset._process_word, phonosem_analyzer, morph_analyzer)
        with multiprocessing.Pool(processes=Dataset.POOL_SIZE) as pool:
            for n, _ in enumerate(pool.imap_unordered(prc_func, dic.items())):
                # print('--')
                pbar.update(n)
        pbar.finish()

    @staticmethod
    def _process_word(analyzer, morph_analyzer, word_item):
        db_conn = MySQLdb.Connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_NAME, use_unicode=True,
                                  charset="utf8")
        word, stresses = word_item
        stresses = list(stresses)
        primary_stress = stresses[0]
        secondary_stress = None
        if len(stresses) > 1:
            secondary_stress = stresses[1]

        with db_conn as db_cursor:
            try:
                sound_word = SoundWord(word, stresses).as_sound_word()

                db_cursor.execute(
                    'INSERT INTO `words`(`word`, `sound_word`, `primary_stress`, `secondary_stress`) '
                    'VALUES (%s, %s, %s, %s)', (word.lower(), sound_word, primary_stress, secondary_stress))
                word_id = db_cursor.lastrowid

                semantic_values = analyzer.analyze_sound_word(sound_word)
                for feature_type_index in range(len(semantic_values)):
                    db_cursor.execute(
                        'INSERT INTO `phonosemantics`(`word_id`, `type_id`, `value`) '
                        'VALUES (%s, %s, %s)',
                        (word_id, feature_type_index + 1, semantic_values[feature_type_index]))

                word_morphs = morph_analyzer.parse(word)
                for word_morph in word_morphs:
                    is_name = {'Name', 'Surn', 'Patr', 'Abbr'} in word_morph.tag
                    is_place = {'Geox', 'Orgn', 'Trad'} in word_morph.tag
                    db_cursor.execute('INSERT INTO `morphemes`(`word_id`, `score`, `tags`, `pos`, '
                                      '`animacy`, `aspect`, `case`, `gender`, `involvement`, `mood`, '
                                      '`number`, `person`, `tense`, `transitivity`, `voice`, '
                                      '`is_name`, `is_place`) VALUES (%s, %s, %s, %s, %s, %s, '
                                      '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                      (word_id, word_morph.score, str(word_morph.tag), word_morph.tag.POS,
                                       word_morph.tag.animacy, word_morph.tag.aspect, word_morph.tag.case,
                                       word_morph.tag.gender, word_morph.tag.involvement,
                                       word_morph.tag.mood,
                                       word_morph.tag.number, word_morph.tag.person, word_morph.tag.tense,
                                       word_morph.tag.transitivity, word_morph.tag.voice, is_name,
                                       is_place))
                db_conn.commit()
            except MySQLdb.IntegrityError:
                # print('Word \'%s\' already exists in database. Skipping...' % word)
                pass
