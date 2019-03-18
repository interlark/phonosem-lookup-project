-- CLEAN UP MESSY DATA
SET SQL_SAFE_UPDATES = 0;
DELETE phonosemantics, morphemes FROM phonosemantics INNER JOIN morphemes
WHERE phonosemantics.word_id = morphemes.word_id AND morphemes.word_id IN
(SELECT words.id FROM words where CONVERT(words.word USING cp1251) REGEXP '^[^[:alpha:]]');
DELETE FROM words WHERE CONVERT(words.word USING cp1251) REGEXP '^[^[:alpha:]]';
SET SQL_SAFE_UPDATES = 1;

-- SWAP WRONG PRIM SECND STRESSES
UPDATE words SET primary_stress=(@temp:=primary_stress), primary_stress = secondary_stress, secondary_stress = @temp
WHERE primary_stress IS NOT NULL AND secondary_stress IS NOT NULL
AND secondary_stress < primary_stress;

-- PHONOSEM TYPES ADDED
INSERT INTO types(name) VALUES
("ХОРОШИЙ-ПЛОХОЙ"),
("БОЛЫШОЙ-МАЛЕНЬКИЙ"),
("НЕЖНЫЙ-ГРУБЫЙ"),
("ЖЕНСТВЕННЫЙ-МУЖЕСТВЕННЫЙ"),
("СВЕТЛЫЙ-ТЕМНЫЙ"),
("АКТИВНЫЙ-ПАССИВНЫЙ"),
("ПРОСТОЙ-СЛОЖНЫЙ"),
("СИЛЬНЫЙ-СЛАБЫЙ"),
("ГОРЯЧИЙ-ХОЛОДНЫЙ"),
("БЫСТРЫЙ-МЕДЛЕННЫЙ"),
("КРАСИВЫЙ-ОТТАЛКИВАЮЩИЙ"),
("ГЛАДКИЙ-ШЕРОХОВАТЫЙ"),
("ЛЕГКИЙ-ТЯЖЕЛЫЙ"),
("ВЕСЕЛЫЙ-ГРУСТНЫЙ"),
("БЕЗОПАСНЫЙ-СТРАШНЫЙ"),
("ВЕЛИЧЕСТВЕННЫЙ-НИЗМЕННЫЙ"),
("ЯРКИЙ-ТУСКЛЫЙ"),
("ОКРУГЛЫЙ-УГЛОВАТЫЙ"),
("РАДОСТНЫЙ-ПЕЧАЛЬНЫЙ"),
("ГРОМКИЙ-ТИХИЙ"),
("ДЛИННЫЙ-КОРОТКИЙ"),
("ХРАБРЫЙ-ТРУСЛИВЫЙ"),
("ДОБРЫЙ-ЗЛОЙ"),
("МОГУЧИЙ-ХИЛЫЙ"),
("ПОДВИЖНЫЙ-МЕДЛИТЕЛЬНЫЙ");

-- FINAL STAGE - COMPOSING WORDS TBL WITH RND ID
CREATE TABLE words_rnd LIKE words;
INSERT INTO words_rnd(id, word, sound_word, primary_stress, secondary_stress) SELECT id, word, sound_word, primary_stress, secondary_stress FROM words ORDER BY rand();
DROP TABLE words;