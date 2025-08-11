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
-- Table structure for table `report_fact`
--

DROP TABLE IF EXISTS `report_fact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `report_fact` (
  `report_fact_id` int NOT NULL AUTO_INCREMENT,
  `date_key` varchar(255) DEFAULT NULL,
  `time_key` varchar(255) DEFAULT NULL,
  `location_key` int DEFAULT NULL,
  `inspector_key` int DEFAULT NULL,
  `supervisor_key` int DEFAULT NULL,
  `asset_key` int DEFAULT NULL,
  `descr` varchar(255) DEFAULT NULL,
  `recc` varchar(255) DEFAULT NULL,
  `ref_no` varchar(255) DEFAULT NULL,
  `region` varchar(255) DEFAULT NULL,
  `inspector_code` varchar(255) DEFAULT NULL,
  `inspection_week` varchar(255) DEFAULT NULL,
  `inspection_code` varchar(255) DEFAULT NULL,
  `is_repeated` tinyint(1) DEFAULT NULL,
  `road_type` varchar(255) DEFAULT NULL,
  `quantity` varchar(255) DEFAULT NULL,
  `measurement` varchar(255) DEFAULT NULL,
  `cause_of_defect` varchar(255) DEFAULT NULL,
  `url_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`report_fact_id`),
  KEY `location_key` (`location_key`),
  KEY `inspector_key` (`inspector_key`),
  KEY `supervisor_key` (`supervisor_key`),
  KEY `asset_key` (`asset_key`),
  CONSTRAINT `report_fact_ibfk_1` FOREIGN KEY (`location_key`) REFERENCES `location_dim` (`location_id`),
  CONSTRAINT `report_fact_ibfk_2` FOREIGN KEY (`inspector_key`) REFERENCES `inspector_dim` (`inspector_id`),
  CONSTRAINT `report_fact_ibfk_3` FOREIGN KEY (`supervisor_key`) REFERENCES `supervisor_dim` (`supervisor_id`),
  CONSTRAINT `report_fact_ibfk_4` FOREIGN KEY (`asset_key`) REFERENCES `asset_dim` (`asset_id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report_fact`
--

LOCK TABLES `report_fact` WRITE;
/*!40000 ALTER TABLE `report_fact` DISABLE KEYS */;
INSERT INTO `report_fact` VALUES (1,'20190520','',1,1,1,1,'damaged','to replace','fc1-w001-001',NULL,NULL,NULL,NULL,1,'major road','3 nos','','faded kerb','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(2,'20190520','',2,1,1,2,'damaged','to replace','fc1-w001-002',NULL,NULL,NULL,NULL,1,'major road','1 nos','','faded kerb','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(3,'20190520','',3,2,1,3,'tilted','to repctify','fc1-w001-003',NULL,NULL,NULL,NULL,1,'major road','1 nos','','faded kerb','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(4,'20190520','',4,1,1,2,'damaged','to replace','fc1-w001-004',NULL,NULL,NULL,NULL,1,'major road','2 nos','','faded kerb','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(5,'20190520','',5,1,1,4,'cracks','to patch','fc1-w001-005',NULL,NULL,NULL,NULL,1,'major road','30m','','paint spillage','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(6,'20190520','',6,2,1,4,'uneven','to patch','fc1-w001-006',NULL,NULL,NULL,NULL,1,'major road','4m x 2m','','paint spillage','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(7,'20190520','',7,1,1,3,'damaged','to replace','fc1-w001-007',NULL,NULL,NULL,NULL,1,'major road','1 nos','','paint spillage','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(8,'20190521','',8,1,1,4,'cracks & depr','to patch','fc1-w001-009',NULL,NULL,NULL,NULL,1,'major road','5m x 2m','','paint spillage','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(9,'20190521','',9,1,1,4,'cracks','to patch','fc1-w001-010',NULL,NULL,NULL,NULL,1,'major road','4m x 2m','','paint spillage','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(10,'20190521','',10,1,1,3,'upside down','to rectify','fc1-w001-011',NULL,NULL,NULL,NULL,1,'major road','1 nos','','paint spillage','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(11,'20190521','',11,1,1,4,'pothole','to patch','fc1-w001-012',NULL,NULL,NULL,NULL,0,'major road','1m x 1m','','paint spillage','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(12,'20190521','',12,1,1,4,'cracks','to patch','fc1-w001-013',NULL,NULL,NULL,NULL,0,'major road','10m x 2m','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(13,'20190521','',13,2,1,5,'faded','to repaint','fc1-w001-015',NULL,NULL,NULL,NULL,0,'major road','50%','','faded kerb','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(14,'20190521','',14,1,1,4,'depression','to patch','fc1-w001-016',NULL,NULL,NULL,NULL,0,'major road','4m x 2m%','','paint spillage','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(15,'20190521','',15,1,1,3,'slanted','to rectify','fc1-w001-017',NULL,NULL,NULL,NULL,0,'major road','1 nos','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(16,'20190521','',16,1,1,5,'faded','to rectify','fc1-w001-018',NULL,NULL,NULL,NULL,0,'major road','50%','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(17,'20190521','',17,1,1,5,'faded','to repaint','fc1-w001-019',NULL,NULL,NULL,NULL,0,'major road','50%','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(18,'20190521','',18,1,1,6,'damaged','to repair','fc1-w001-020',NULL,NULL,NULL,NULL,0,'major road','4 panel (10m)','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(19,'20190521','',19,3,1,4,'peel off','to patch','fc1-w001-021',NULL,NULL,NULL,NULL,0,'major road','1m x 1m','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(20,'20190521','',20,1,1,1,'damaged','to replace','fc1-w001-022',NULL,NULL,NULL,NULL,0,'major road','1 nos','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(21,'20190521','',21,2,1,1,'damaged','refer ro','fc1-w001-023',NULL,NULL,NULL,NULL,0,'major road','5m','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(22,'20190521','',22,1,1,2,'damaged','to replace','fc1-w001-024',NULL,NULL,NULL,NULL,0,'major road','1 nos','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(23,'20190521','',23,1,1,3,'slanted','to rectify','fc1-w001-025',NULL,NULL,NULL,NULL,0,'major road','1 nos','','trench','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(24,'20190521','',24,3,1,4,'peel off','to patch','fc1-w001-026',NULL,NULL,NULL,NULL,0,'major road','2m x 2m','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(25,'20190521','',25,1,1,1,'damaged','refer ro','fc1-w001-028',NULL,NULL,NULL,NULL,0,'major road','10m','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(26,'20190521','',26,1,1,4,'concrete drop','to remove','fc1-w001-029',NULL,NULL,NULL,NULL,0,'major road','10m','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(27,'20190521','',27,1,1,1,'damaged','refer ro','fc1-w001-031',NULL,NULL,NULL,NULL,0,'major road','100m','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(28,'20190521','',28,1,1,1,'damaged','refer ro','fc1-w001-032',NULL,NULL,NULL,NULL,0,'major road','10m','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(29,'20190521','',29,1,1,3,'tilted','to rectify','fc1-w001-033',NULL,NULL,NULL,NULL,0,'major road','1 nos','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(30,'20190522','',30,1,1,1,'damaged','to replace','fc1-w001-034',NULL,NULL,NULL,NULL,0,'major road','1 nos','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(31,'20190522','',31,1,1,7,'damaged','to patch','fc1-w001-035',NULL,NULL,NULL,NULL,0,'major road','3m x 2m','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(32,'20190522','',32,1,1,4,'cracks','to patch','fc1-w001-036',NULL,NULL,NULL,NULL,0,'major road','50m','','faded kerb','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(33,'20190522','',33,1,1,4,'ravelling','to patch','fc1-w001-037',NULL,NULL,NULL,NULL,0,'major road','3m x 2m','','faded kerb','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(34,'20190522','',34,1,1,4,'ravelling','to patch','fc1-w001-038',NULL,NULL,NULL,NULL,0,'major road','4m x 2m','','faded kerb','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(35,'20190522','',35,1,1,4,'cracks','to seal','fc1-w001-039',NULL,NULL,NULL,NULL,0,'major road','10m x 1m','','faded kerb','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(36,'20190522','',36,1,1,4,'cracks','to seal','fc1-w001-040',NULL,NULL,NULL,NULL,0,'major road','5m x 2m','','faded kerb','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(37,'20190522','',37,1,1,4,'peel off','to patch','fc1-w001-041',NULL,NULL,NULL,NULL,0,'major road','2m x 2m','','faded kerb','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(38,'20190522','',38,1,1,4,'ravelling  & p','to patch','fc1-w001-042',NULL,NULL,NULL,NULL,0,'major road','4m x 2m','','faded kerb','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(39,'20190522','',39,1,1,5,'faded','to repaint','fc1-w001-043',NULL,NULL,NULL,NULL,0,'major road','50%','','faded kerb','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(40,'20190522','',40,1,1,4,'cracks & corr','to repaint','fc1-w001-044',NULL,NULL,NULL,NULL,0,'major road','50%','','faded kerb','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(41,'20190522','',41,1,1,4,'cracks','to patch','fc1-w001-045',NULL,NULL,NULL,NULL,0,'major road','100m','','faded kerb','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(42,'20190522','',42,1,1,4,'cracks','to patch','fc1-w001-046',NULL,NULL,NULL,NULL,0,'major road','4m x 2m','','faded kerb','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(43,'20190522','',43,1,1,2,'damaged','to replace','fc1-w001-047',NULL,NULL,NULL,NULL,0,'major road','1 nos','','faded kerb','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(44,'20190522','',44,1,1,4,'cracks & depr','to patch','fc1-w001-048',NULL,NULL,NULL,NULL,0,'major road','4m x 2m','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(45,'20190522','',45,1,1,1,'damaged','to replace','fc1-w001-049',NULL,NULL,NULL,NULL,0,'major road','1 nos','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(46,'20190522','',46,1,1,4,'cracks & peel','to patch','fc1-w001-050',NULL,NULL,NULL,NULL,0,'major road','4m x 2m','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(47,'20190522','',47,1,1,4,'cracks','to patch','fc1-w001-051',NULL,NULL,NULL,NULL,0,'major road','50m x 2m','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(48,'20190522','',48,1,1,4,'ravelling','to patch','fc1-w001-052',NULL,NULL,NULL,NULL,0,'major road','5m x 4m','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(49,'20190522','',49,1,1,4,'peel off','to patch','fc1-w001-053',NULL,NULL,NULL,NULL,0,'major road','1m x 1m','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(50,'20190522','',50,1,1,4,'cracks','to patch','fc1-w001-054',NULL,NULL,NULL,NULL,0,'major road','5m x 2m','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(51,'20190522','',51,1,1,4,'cracks','to patch','fc1-w001-055',NULL,NULL,NULL,NULL,0,'major road','5m x 2m','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(52,'20190522','',52,1,1,4,'cracks','to patch','fc1-w001-057',NULL,NULL,NULL,NULL,0,'major road','2m x 2m','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(53,'20190522','',53,1,1,4,'cracks','to patch','fc1-w001-058',NULL,NULL,NULL,NULL,0,'major road','3m x 2m','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(54,'20190523','',54,1,1,3,'tilted','to rectify','fc1-w001-059',NULL,NULL,NULL,NULL,0,'major road','1 nos','','missing grate','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(55,'20190523','',55,1,1,2,'damaged','to replace','fc1-w001-060',NULL,NULL,NULL,NULL,0,'major road','1 nos','','paint spillage','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(56,'20190523','',56,1,1,4,'cracks','to patch','fc1-w001-061',NULL,NULL,NULL,NULL,0,'major road','5m x 1m','','paint spillage','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf'),(57,'20190523','',57,1,1,4,'ravelling','to patch','fc1-w001-062',NULL,NULL,NULL,NULL,0,'major road','3m x 2m','','paint spillage','CYCLE_1/WEEK 001/20190522/BIDEFORD ROAD/FC2-W001-049.pdf');
/*!40000 ALTER TABLE `report_fact` ENABLE KEYS */;
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
