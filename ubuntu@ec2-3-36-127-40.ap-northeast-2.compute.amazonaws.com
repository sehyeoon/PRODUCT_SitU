-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
--
-- Host: localhost    Database: situ
-- ------------------------------------------------------
-- Server version	8.0.20

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts_cafe`
--

DROP TABLE IF EXISTS `accounts_cafe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_cafe` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `last_login` datetime(6) DEFAULT NULL,
  `cafe_id` varchar(50) NOT NULL,
  `name` varchar(255) NOT NULL,
  `telephone` varchar(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cafe_id` (`cafe_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_cafe`
--

LOCK TABLES `accounts_cafe` WRITE;
/*!40000 ALTER TABLE `accounts_cafe` DISABLE KEYS */;
INSERT INTO `accounts_cafe` VALUES (2,'2024-07-17 03:27:45.388962','store_001','카페파인','02-926-3726','pbkdf2_sha256$720000$mQgfR8MvsOPEBUoAmEyKMa$RU4UnVHWYc8qWeUMPtq/pGC05o1XFrqyglChc6ltH4A=',1,0,0),(3,NULL,'store_002','빈트리','098-765-4321','pbkdf2_sha256$720000$PAIPYPdiZYgU9wat2f9AV5$2Ev5XeLEgRjJqTLDLlx+DhY7lPDiwyXABut8XOfEllU=',1,0,0);
/*!40000 ALTER TABLE `accounts_cafe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add cafe',6,'add_cafe'),(22,'Can change cafe',6,'change_cafe'),(23,'Can delete cafe',6,'delete_cafe'),(24,'Can view cafe',6,'view_cafe'),(25,'Can add seat',7,'add_seat'),(26,'Can change seat',7,'change_seat'),(27,'Can delete seat',7,'delete_seat'),(28,'Can view seat',7,'view_seat');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_cafe_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_cafe_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_cafe` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (6,'accounts','cafe'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(7,'reservations','seat'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'accounts','0001_initial','2024-07-14 08:39:53.038319'),(2,'contenttypes','0001_initial','2024-07-14 08:39:53.119506'),(3,'admin','0001_initial','2024-07-14 08:39:53.385079'),(4,'admin','0002_logentry_remove_auto_add','2024-07-14 08:39:53.404477'),(5,'admin','0003_logentry_add_action_flag_choices','2024-07-14 08:39:53.419993'),(6,'contenttypes','0002_remove_content_type_name','2024-07-14 08:39:53.615876'),(7,'auth','0001_initial','2024-07-14 08:39:54.138226'),(8,'auth','0002_alter_permission_name_max_length','2024-07-14 08:39:54.288653'),(9,'auth','0003_alter_user_email_max_length','2024-07-14 08:39:54.303372'),(10,'auth','0004_alter_user_username_opts','2024-07-14 08:39:54.315474'),(11,'auth','0005_alter_user_last_login_null','2024-07-14 08:39:54.337195'),(12,'auth','0006_require_contenttypes_0002','2024-07-14 08:39:54.337195'),(13,'auth','0007_alter_validators_add_error_messages','2024-07-14 08:39:54.353039'),(14,'auth','0008_alter_user_username_max_length','2024-07-14 08:39:54.411106'),(15,'auth','0009_alter_user_last_name_max_length','2024-07-14 08:39:54.424214'),(16,'auth','0010_alter_group_name_max_length','2024-07-14 08:39:54.498447'),(17,'auth','0011_update_proxy_permissions','2024-07-14 08:39:54.519783'),(18,'auth','0012_alter_user_first_name_max_length','2024-07-14 08:39:54.533779'),(19,'reservations','0001_initial','2024-07-14 08:39:54.854929'),(20,'sessions','0001_initial','2024-07-14 08:39:54.973960');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('4htl1f34v4fb0u8wj54kk8c5prdam8f3','.eJxVizsKAjEQQO-SWpbEfMdSbKw9QJjMZIgIu7DZVOLdVdhC2_d5qoxja3n0uuY7q5M6qsMvK0iPOn8FEi1j3vq0oz7dtmWt18t5T_6-hr19Ju-jlBRjZUManGZkqBGtAUfAVpxYEwwAuZKCFkFLAhZKSIWN9qheb7ykNLA:1sTvKT:3WIh2RZKfULQj4nSDqSAqVn2_vzsqfbyczde8YfxVPY','2024-07-31 03:27:45.397468'),('9uuj0ftxfimygx51sevn2kcd6ecnz6ya','.eJxVizsKAjEQQO-SWpbEfMdSbKw9QJjMZIgIu7DZVOLdVdhC2_d5qoxja3n0uuY7q5M6qsMvK0iPOn8FEi1j3vq0oz7dtmWt18t5T_6-hr19Ju-jlBRjZUManGZkqBGtAUfAVpxYEwwAuZKCFkFLAhZKSIWN9qheb7ykNLA:1sSusQ:Ozi9kL_0AmHLz7g4gu3GYbUWS_Is_FIdQXdSwKXoJHo','2024-07-28 08:46:38.747326'),('wwxuoqxoo29o8lyg2wl8vwf1kzkbubj5','e30:1sSupK:wE0C9XODcfQ0q0Uai9sPLXrO0jNHDJTyPkxGs3caAlY','2024-07-28 08:43:26.068409');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seats`
--

DROP TABLE IF EXISTS `seats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seats` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `seat_status` varchar(10) NOT NULL,
  `plug` tinyint(1) DEFAULT NULL,
  `backseat` tinyint(1) DEFAULT NULL,
  `seat_start_time` datetime(6) DEFAULT NULL,
  `seat_use_time` bigint DEFAULT NULL,
  `seats_no` int DEFAULT NULL,
  `seats_count` int DEFAULT NULL,
  `empty_seats` int DEFAULT NULL,
  `cafe_id` bigint NOT NULL,
  `seat_user_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `seats_cafe_id_690f229a_fk_accounts_cafe_id` (`cafe_id`),
  KEY `seats_seat_user_id_f0d98eb9_fk_accounts_cafe_id` (`seat_user_id`),
  CONSTRAINT `seats_cafe_id_690f229a_fk_accounts_cafe_id` FOREIGN KEY (`cafe_id`) REFERENCES `accounts_cafe` (`id`),
  CONSTRAINT `seats_seat_user_id_f0d98eb9_fk_accounts_cafe_id` FOREIGN KEY (`seat_user_id`) REFERENCES `accounts_cafe` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seats`
--

LOCK TABLES `seats` WRITE;
/*!40000 ALTER TABLE `seats` DISABLE KEYS */;
INSERT INTO `seats` VALUES (1,'available',NULL,NULL,NULL,NULL,1,NULL,NULL,2,NULL),(2,'available',NULL,NULL,NULL,NULL,2,NULL,NULL,2,NULL),(3,'available',NULL,NULL,NULL,NULL,3,NULL,NULL,2,NULL),(4,'available',NULL,NULL,NULL,NULL,4,NULL,NULL,2,NULL),(5,'occupied',NULL,NULL,'2024-07-17 03:51:38.564142',NULL,5,NULL,NULL,2,NULL);
/*!40000 ALTER TABLE `seats` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-17 13:57:37
