## Фоносемантический поиск слов

[![Python 3.6](https://img.shields.io/badge/Python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![License](https://img.shields.io/badge/License-Apache%202.0-orange.svg)](https://opensource.org/licenses/Apache-2.0)

#### Установка
```bash
git clone https://github.com/interlark/phonosem-lookup-project
cd phonosem-lookup-project
pip3 install -r requirements.txt
```

#### Использование

##### Загрузка словаря
```bash
wget -P data https://www.dropbox.com/s/1gl7ltx3kkg1dro/pronouncing.dict
```

##### Подготовка данных

###### Создание структуры БД
```bash
$ mysql -u root -p
```

```mysql
mysql> CREATE DATABASE words_dataset CHARACTER SET utf8 COLLATE utf8_general_ci;
```

```bash
$ mysql -u username -p words_dataset < data/mysql/db_schema.sql
```

###### Создание датасета

```bash
$ python3 create_dataset.py --help
```

```text
usage: create_dataset.py [-h] dict_file freq_table sign_table

Dataset composing and creating tool.

positional arguments:
  dict_file   pronouncing dictionary file
  freq_table  frequency csv table
  sign_table  significance csv table

optional arguments:
  -h, --help  show this help message and exit
```

```bash
$ python3 create_dataset.py data/pronouncing.dict \
data/sound_letters_frequency.csv \
data/sound_letters_significance.csv
```

###### Постобработка датасета

```bash
$ mysql -u username -p words_dataset < data/mysql/clean_up.sql
```

##### Создание модели

Ниже приведены примеры создания упрощенных моделей генерации слов по фоносемантическим признакам.

Существительное (им.п, ед. число, исключены знаки, 6 символов, одно ударение),
```bash
jupyter notebook phonosem_model_noun.ipynb
```

Прилагательное (полное, им.п, ед. число, исключены знаки, 9 символов, одно ударение), 
```bash
jupyter notebook phonosem_model_adjf.ipynb
```

##### Генерация слов

Генерирование слова по одному из фоносемантических признаков указанных в *[1]*.

```bash
$ python3 lookup.py --help
```

```text
usage: lookup.py [-h] [--skip-inappropriate]
                 freq_table sign_table model feature_idx {LEFT,RIGHT}

Simple phonosemantic word lookup based on machine learning.

positional arguments:
  freq_table            frequency csv table
  sign_table            significance csv table
  model                 model file
  feature_idx           feature index
  {LEFT,RIGHT}          feature direction

optional arguments:
  -h, --help            show this help message and exit
  --skip-inappropriate  skip inappropriate words

```

Существительное (им.п, ед. число, исключены знаки, 6 символов, одно ударение), шкала СИЛЬНЫЙ-СЛАБЫЙ, признак СЛАБЫЙ, RIGHT (значимость ≥ 3.5),

```bash
$ python3 lookup.py data/sound_letters_frequency.csv \
data/sound_letters_significance.csv \
current_noun_6_scaled.h5 \
7 RIGHT --skip-inappropriate
```

```text
Сгенерированное звуко-слово: п'лю'хмя
Полученное значение признака: 3.843123649931269

Сгенерированное звуко-слово: д'х'о'жн'я
Полученное значение признака: 3.933472390272441
```

Прилагательное (полное, им.п, ед. число, исключены знаки, 9 символов, одно ударение), шкала ДЛИННЫЙ-КОРОТКИЙ, признак ДЛИННЫЙ, LEFT (значимость  ≤ 2.5),

```bash
$ python3 lookup.py data/sound_letters_frequency.csv \
data/sound_letters_significance.csv \
current_adjf_9_scaled.h5 \
20 LEFT --skip-inappropriate
```

```text
Сгенерированное звуко-слово: э'мд'у'р'ф'ный
Полученное значение признака: 2.4184793955874846

Сгенерированное звуко-слово: ы'жчу'у'кный
Полученное значение признака: 2.3646604938271607
```

#### Примечание

Таблица частотности звукобукв и таблица фоносемантической значимости звукобукв расположенны соответственно в

```text
data/sound_letters_frequency.csv 
```

и

```text
data/sound_letters_significance.csv
```

#### [1] Таблица шкал фоносемантических признаков


| Index |  Left          |  Right        | 
|-------|----------------|---------------| 
| 0     | ХОРОШИЙ        | ПЛОХОЙ        | 
| 1     | БОЛЬШОЙ        | МАЛЕНЬКИЙ     | 
| 2     | НЕЖНЫЙ         | ГРУБЫЙ        | 
| 3     | ЖЕНСТВЕННЫЙ    | МУЖЕСТВЕННЫЙ  | 
| 4     | СВЕТЛЫЙ        | ТЕМНЫЙ        | 
| 5     | АКТИВНЫЙ       | ПАССИВНЫЙ     | 
| 6     | ПРОСТОЙ        | СЛОЖНЫЙ       | 
| 7     | СИЛЬНЫЙ        | СЛАБЫЙ        | 
| 8     | ГОРЯЧИЙ        | ХОЛОДНЫЙ      | 
| 9     | БЫСТРЫЙ        | МЕДЛЕННЫЙ     | 
| 10    | КРАСИВЫЙ       | ОТТАЛКИВАЮЩИЙ | 
| 11    | ГЛАДКИЙ        | ШЕРОХОВАТЫЙ   | 
| 12    | ЛЕГКИЙ         | ТЯЖЕЛЫЙ       | 
| 13    | ВЕСЕЛЫЙ        | ГРУСТНЫЙ      | 
| 14    | БЕЗОПАСНЫЙ     | СТРАШНЫЙ      | 
| 15    | ВЕЛИЧЕСТВЕННЫЙ | НИЗМЕННЫЙ     | 
| 16    | ЯРКИЙ          | ТУСКЛЫЙ       | 
| 17    | ОКРУГЛЫЙ       | УГЛОВАТЫЙ     | 
| 18    | РАДОСТНЫЙ      | ПЕЧАЛЬНЫЙ     | 
| 19    | ГРОМКИЙ        | ТИХИЙ         | 
| 20    | ДЛИННЫЙ        | КОРОТКИЙ      | 
| 21    | ХРАБРЫЙ        | ТРУСЛИВЫЙ     | 
| 22    | ДОБРЫЙ         | ЗЛОЙ          | 
| 23    | МОГУЧИЙ        | ХИЛЫЙ         | 
| 24    | ПОДВИЖНЫЙ      | МЕДЛИТЕЛЬНЫЙ  | 

#### Литература

1. Журавлев А.П. Звук и смысл / А.П. Журавлев. - М. : Просвещение, 1991. - 160 с.
2. Санжаров Л.Н. Современная фоносемантика: истоки, проблемы, возможные решения / Л.Н. Санжаров. - Тула : Издательство Тульского педагогического университета, 1996. - 33 с.
3. Черепанова И.Ю. Клич Гамаюн / И.Ю. Черепанова. - М. : Профит Стайл, 2007. - 464 с.