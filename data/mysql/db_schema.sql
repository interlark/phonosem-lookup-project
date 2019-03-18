-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: localhost    Database: words_dataset
-- ------------------------------------------------------
-- Server version	5.7.25-0ubuntu0.18.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `morphemes`
--

DROP TABLE IF EXISTS `morphemes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `morphemes` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `word_id` bigint(20) unsigned NOT NULL,
  `score` float DEFAULT NULL,
  `tags` text,
  `pos` varchar(4) DEFAULT NULL,
  `animacy` varchar(4) DEFAULT NULL,
  `aspect` varchar(4) DEFAULT NULL,
  `case` varchar(4) DEFAULT NULL,
  `gender` varchar(4) DEFAULT NULL,
  `involvement` varchar(4) DEFAULT NULL,
  `mood` varchar(4) DEFAULT NULL,
  `number` varchar(4) DEFAULT NULL,
  `person` varchar(4) DEFAULT NULL,
  `tense` varchar(4) DEFAULT NULL,
  `transitivity` varchar(4) DEFAULT NULL,
  `voice` varchar(4) DEFAULT NULL,
  `is_name` bit(1) DEFAULT NULL,
  `is_place` bit(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `morphemes_word_idx` (`word_id`) USING BTREE,
  KEY `morphemes_score_idx` (`score`) USING BTREE,
  KEY `morphemes_pos_idx` (`pos`) USING BTREE,
  KEY `morphemes_animacy_idx` (`animacy`) USING BTREE,
  KEY `morphemes_aspect_idx` (`aspect`) USING BTREE,
  KEY `morphemes_case_idx` (`case`) USING BTREE,
  KEY `morphemes_gender_idx` (`gender`) USING BTREE,
  KEY `morphemes_involvement_idx` (`involvement`) USING BTREE,
  KEY `morphemes_mood_idx` (`mood`) USING BTREE,
  KEY `morphemes_number_idx` (`number`) USING BTREE,
  KEY `morphemes_person_idx` (`person`) USING BTREE,
  KEY `morphemes_tense_idx` (`tense`) USING BTREE,
  KEY `morphemes_transitivity_idx` (`transitivity`) USING BTREE,
  KEY `morphemes_voice_idx` (`voice`) USING BTREE,
  KEY `morphemes_is_name_idx` (`is_name`) USING BTREE,
  KEY `morphemes_is_place_idx` (`is_place`) USING BTREE,
  CONSTRAINT `fk_morphemes_word` FOREIGN KEY (`word_id`) REFERENCES `words` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2718106 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phonosemantics`
--

DROP TABLE IF EXISTS `phonosemantics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phonosemantics` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `word_id` bigint(20) unsigned NOT NULL,
  `type_id` int(11) unsigned NOT NULL,
  `value` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `phonosemantics_value_idx` (`value`) USING BTREE,
  KEY `fk_phonosemantics_type_idx` (`type_id`) USING BTREE,
  KEY `fk_phonosemantics_word_idx` (`word_id`),
  KEY `id_word_id_idx` (`id`,`word_id`) USING BTREE,
  CONSTRAINT `fk_phonosemantics_type` FOREIGN KEY (`type_id`) REFERENCES `types` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_phonosemantics_word` FOREIGN KEY (`word_id`) REFERENCES `words` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=76753351 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `types`
--

DROP TABLE IF EXISTS `types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `types` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(25) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `words`
--

DROP TABLE IF EXISTS `words`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `words` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `word` varchar(30) NOT NULL,
  `sound_word` varchar(60) DEFAULT NULL,
  `primary_stress` tinyint(3) unsigned NOT NULL,
  `secondary_stress` tinyint(3) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `word_UNIQUE` (`word`),
  KEY `words_idx` (`word`) USING BTREE,
  KEY `word_stress_primary_idx` (`primary_stress`) USING BTREE,
  KEY `word_stress_secondary_idx` (`secondary_stress`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1538699 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `words_rnd`
--

DROP TABLE IF EXISTS `words_rnd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `words_rnd` (
  `id` bigint(20) unsigned NOT NULL,
  `rnd_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `word` varchar(30) NOT NULL,
  `sound_word` varchar(60) DEFAULT NULL,
  `primary_stress` tinyint(3) unsigned NOT NULL,
  `secondary_stress` tinyint(3) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `word_UNIQUE` (`word`),
  UNIQUE KEY `rnd_id_UNIQUE` (`rnd_id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `words_idx` (`word`) USING BTREE,
  KEY `word_stress_primary_idx` (`primary_stress`) USING BTREE,
  KEY `word_stress_secondary_idx` (`secondary_stress`) USING BTREE,
  KEY `rnd_id_idx` (`rnd_id`) USING BTREE,
  KEY `rnd_id_id_idx` (`id`,`rnd_id`) USING BTREE,
  KEY `rnd_id_stress_secondary_idx` (`rnd_id`,`secondary_stress`) USING BTREE,
  KEY `rnd_id_stress_primary_idx` (`rnd_id`,`primary_stress`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1535042 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-03-15 19:09:29
