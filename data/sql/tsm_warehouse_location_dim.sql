-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: tsm_warehouse
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `location_dim`
--

DROP TABLE IF EXISTS `location_dim`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `location_dim` (
  `location_id` int NOT NULL AUTO_INCREMENT,
  `lampost_id` varchar(255) DEFAULT NULL,
  `location_1` varchar(255) DEFAULT NULL,
  `location_2` varchar(255) DEFAULT NULL,
  `road_type_1` varchar(255) DEFAULT NULL,
  `road_type_2` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`location_id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `location_dim`
--

LOCK TABLES `location_dim` WRITE;
/*!40000 ALTER TABLE `location_dim` DISABLE KEYS */;
INSERT INTO `location_dim` VALUES (1,'85','upper seranggon road',NULL,NULL,NULL),(2,'145','upper seranggon road',NULL,NULL,NULL),(3,'151','upper seranggon road',NULL,NULL,NULL),(4,'171','upper seranggon road',NULL,NULL,NULL),(5,'217','upper seranggon road',NULL,NULL,NULL),(6,'229','upper seranggon road',NULL,NULL,NULL),(7,'138','upper seranggon road',NULL,NULL,NULL),(8,'87','upper seranggon road',NULL,NULL,NULL),(9,'152','upper seranggon road',NULL,NULL,NULL),(10,'87/2','upper seranggon road',NULL,NULL,NULL),(11,'84/25','upper seranggon road',NULL,NULL,NULL),(12,'84/11','upper seranggon road',NULL,NULL,NULL),(13,'39-lp38','jalan kayu',NULL,NULL,NULL),(14,'33','punggol central',NULL,NULL,NULL),(15,'87','punggol central',NULL,NULL,NULL),(16,'147','punggol central',NULL,NULL,NULL),(17,'7','punggol east',NULL,NULL,NULL),(18,'151','punggol field',NULL,NULL,NULL),(19,'15','punggol field',NULL,NULL,NULL),(20,'12','seletar aerospace way',NULL,NULL,NULL),(21,'48','sengkang east drive',NULL,NULL,NULL),(22,'142','sengkang east way',NULL,NULL,NULL),(23,'104','sengkang east way',NULL,NULL,NULL),(24,'74','sengkang east way',NULL,NULL,NULL),(25,'37','sengkang west road',NULL,NULL,NULL),(26,'21','sengkang west road',NULL,NULL,NULL),(27,'30','sengkang west road',NULL,NULL,NULL),(28,'60','sengkang west road',NULL,NULL,NULL),(29,'180/1','sengkang west way',NULL,NULL,NULL),(30,'13','cantonment road',NULL,NULL,NULL),(31,'11','cantonment road',NULL,NULL,NULL),(32,'11-lp9','cantonment road',NULL,NULL,NULL),(33,'42','bras basah road',NULL,NULL,NULL),(34,'72','bras basah road',NULL,NULL,NULL),(35,'75s1f','bras basah road',NULL,NULL,NULL),(36,'3','cairnhill road',NULL,NULL,NULL),(37,'18','cairnhill road',NULL,NULL,NULL),(38,'18','cairnhill road',NULL,NULL,NULL),(39,'21-lp25','cairnhill road',NULL,NULL,NULL),(40,'37','eu tong sen street',NULL,NULL,NULL),(41,'56-lp59','eu tong sen street',NULL,NULL,NULL),(42,'31','grange road',NULL,NULL,NULL),(43,'31','grange road',NULL,NULL,NULL),(44,'49','grange road',NULL,NULL,NULL),(45,'58','grange road',NULL,NULL,NULL),(46,'49','grange road',NULL,NULL,NULL),(47,'3-lp4','hoot kiam road',NULL,NULL,NULL),(48,'11','hoot kiam road',NULL,NULL,NULL),(49,'17','neil road',NULL,NULL,NULL),(50,'58','orchard road',NULL,NULL,NULL),(51,'10','orchard road',NULL,NULL,NULL),(52,'6/1f','paterson road',NULL,NULL,NULL),(53,'8','paterson hill',NULL,NULL,NULL),(54,'67','river valley road',NULL,NULL,NULL),(55,'73','river valley road',NULL,NULL,NULL),(56,'60','scotts road',NULL,NULL,NULL),(57,'30','scotts road',NULL,NULL,NULL);
/*!40000 ALTER TABLE `location_dim` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-11 10:18:56
