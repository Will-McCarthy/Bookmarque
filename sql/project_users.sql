-- MySQL dump 10.13  Distrib 8.0.23, for macos10.15 (x86_64)
--
-- Host: localhost    Database: project
-- ------------------------------------------------------
-- Server version	8.0.23

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
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `userID` int NOT NULL AUTO_INCREMENT COMMENT 'Identifies Web Users, Admins, and Customers.',
  `userEmail` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'Needs to be unique for non-web users.',
  `userFName` varchar(45) DEFAULT NULL,
  `userLName` varchar(45) DEFAULT NULL,
  `userStatus` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'Either Active, Inactive, or Suspended.',
  `userType` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'Either Web User, Customer, or Admin.',
  `userPassword` varchar(250) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `userPhone` varchar(45) DEFAULT NULL,
  `userSubStatus` varchar(45) DEFAULT NULL,
  `addressID` int DEFAULT NULL COMMENT 'Can be null to account for the optional address field.',
  PRIMARY KEY (`userID`),
  UNIQUE KEY `userEmail_UNIQUE` (`userEmail`),
  KEY `fk_users_address1_idx` (`addressID`)
) ENGINE=InnoDB AUTO_INCREMENT=108 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (101,'janedoe@gmail.com','Jane','Jones','Active','Customer','gAAAAABgfsYmwAh_G-RdRRytYzXLtz5prbXyQj2O0zBzoyPepRsIgVwhr51_Auhl_nH4jhHzMmeYADnipmYgdjVIaiEZ5eigaA==','123-456-2558','Active',105),(102,'johndoe@gmail.com','John','Doe','Active','Customer','gAAAAABgfsYmyQIg3PKAiNzMbFv40RfjkzUXjRWvA94LzmQWoEvqYDwM8qnfMoV0DGapURdI_tleiD3LeQRhI-RC1uZJAr2PvQ==','971-221-8787','Active',101),(103,'jimmycricket@uga.edu','Jimmy','Cricket','Active','Admin','gAAAAABgfsYmTLfqdrx2bl1yn-6_i9uHjmNdcdKaEfHthOAM26ihBVh3NGPwmnBdtgdnDpty-qnMEdOrIkXx2XainUBu2JHQjQ==','124-458-9989','Deactive',NULL),(104,'petergriffin@yahoo.com','Peter','Griffin','Suspended','Customer','gAAAAABgfsYmzQSPTg1q4yb6ypYrpiLxLhlrnkYd2nOOECwxy6haScDh7q5gXicovRRGiTVAdlsf04S4uaoHGvzC8s0fofoGBg==','245-545-7777','Deactive',104),(105,NULL,NULL,NULL,NULL,'Web User','gAAAAABgfsYm6Av14KsOTBmaSAxW8-_4Ov2suEsUyKe2FOYbB2YjHJxSNqLv2aHPgRgUGqNEfoUWI2o-JOD0As6HosqxREixGw==',NULL,NULL,NULL),(106,'johnsnow@gmail.com','John','Snow','Inactive','Customer','gAAAAABgfsYmK4eW4hqDuUCr4AR_e8XPo-SSFHQCJrtpUzQO1frWqbHnPaI447KDejjlRnsPF22ZqrQqDH1JcYs53rk8gVrxlQ==','656-221-6240','Deactive',NULL),(107,'lebronjames@yahoo.com','Lebron','James','Active','Customer','gAAAAABgfsYmHgwv-xhYTqsqj1lHmlGLaWIffDLt8dWeB8EbgKyofvcQJtcXcVlHKEZqpsm_XV8CNSMSTU2xDaLtIWyzUbaUaA==','987-145-6654','Active',103);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-04-20  8:22:13
