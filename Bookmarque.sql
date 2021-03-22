-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: bookmarque
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
-- Table structure for table `address`
--

DROP TABLE IF EXISTS `address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `address` (
  `addressID` int NOT NULL COMMENT 'Identifies customer addresses.',
  `addressStreet` varchar(45) DEFAULT NULL,
  `addressCity` varchar(45) DEFAULT NULL,
  `addressState` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`addressID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address`
--

LOCK TABLES `address` WRITE;
/*!40000 ALTER TABLE `address` DISABLE KEYS */;
INSERT INTO `address` VALUES (101,'123 Generic Street','Athens','GA'),(102,'245 Mario Lane','San Francisco','CA'),(103,'987 Sunset Boulevard','Los Angeles','CA'),(104,'221 Baked Alaska Way','Miami','FL');
/*!40000 ALTER TABLE `address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book`
--

DROP TABLE IF EXISTS `book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book` (
  `ISBN` char(13) NOT NULL,
  `bookTitle` varchar(115) DEFAULT NULL,
  `authorFName` varchar(45) DEFAULT NULL,
  `authorLName` varchar(45) DEFAULT NULL,
  `bookImage` blob,
  `bookPrice` double DEFAULT NULL,
  `bookQuantity` int DEFAULT NULL,
  `bookRating` int DEFAULT NULL,
  `bookPublisher` varchar(45) DEFAULT NULL,
  `bookPublicationDate` datetime DEFAULT NULL,
  `bookDescription` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`ISBN`),
  UNIQUE KEY `ISBN-13_UNIQUE` (`ISBN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book`
--

LOCK TABLES `book` WRITE;
/*!40000 ALTER TABLE `book` DISABLE KEYS */;
INSERT INTO `book` VALUES ('9780063012196','The Divines','Ellie','Eaton',NULL,20.39,11,4,'William Morrow','2021-01-19 00:00:00',NULL),('9780307958198','Black Hole Blues and Other Songs from Outer Space','Janna','Levin',NULL,22.19,7,4,'Knopf','2016-03-29 00:00:00',NULL),('9780385537674','Fifty Shades of Grey','Erika','Leonard',NULL,26.95,13,4,'Doubleday','2013-01-29 00:00:00',NULL),('9780451493095','All We Saw','Anne','Michaels',NULL,17,14,5,'Knopf','2017-10-03 00:00:00',NULL),('9780593311684','The Cheffe: A Cook\'s Novel','Marie','NDiaye',NULL,22.99,15,4,'Vintage','2021-01-19 00:00:00',NULL),('9781101994979','That Inevitable Victorian Thing','Emily','Johnston',NULL,8.99,20,3,'Dutton Books for Young Readers','2017-10-03 00:00:00',NULL),('9781250126627','A Selfie as Big as the Ritz','Lara','Williams',NULL,9.95,4,4,'Flatiron Books','2017-10-31 00:00:00',NULL),('9781594633881','The Vacationers','Emma','Straub',NULL,25.99,9,3,'Penguin Publishing Group','2014-06-02 00:00:00','For the Posts, a two-week trip to the Balearic island of Mallorca with their extended family and friends is a celebration: Franny and Jim are observing their thirty-fifth wedding anniversary, and their daughter, Sylvia, has graduated from high school. The sunlit island, its mountains and beaches, its tapas and tennis courts, also promise an escape from the tensions simmering at home in Manhattan. But all does not go according to plan: over the course of the vacation, secrets come to light, old and new humiliations are experienced, childhood rivalries resurface, and ancient wounds are exacerbated.'),('9781594634109','Hiding in Plain Sight','Nuruddin','Farah',NULL,18,5,3,'Riverhead Books','2015-09-22 00:00:00',NULL);
/*!40000 ALTER TABLE `book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_categories`
--

DROP TABLE IF EXISTS `book_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_categories` (
  `categoryID` int NOT NULL,
  `categoryName` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'Book category/genre.',
  PRIMARY KEY (`categoryID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_categories`
--

LOCK TABLES `book_categories` WRITE;
/*!40000 ALTER TABLE `book_categories` DISABLE KEYS */;
INSERT INTO `book_categories` VALUES (1,'Featured'),(2,'Education'),(3,'Domestic Fiction'),(4,'Drama'),(5,'Classic'),(6,'Thriller'),(7,'Romance'),(8,'History'),(9,'Young Adult'),(10,'Esoteric'),(11,'Science Fiction'),(12,'Science'),(13,'Self-Help'),(14,'Non-Fiction'),(15,'Horror'),(16,'Business'),(17,'Short Stories');
/*!40000 ALTER TABLE `book_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_has_book_categories`
--

DROP TABLE IF EXISTS `book_has_book_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_has_book_categories` (
  `ISBN` char(13) NOT NULL,
  `categoryID` int NOT NULL,
  PRIMARY KEY (`ISBN`,`categoryID`),
  KEY `fk_book_has_book_catagories_book_catagories1_idx` (`categoryID`),
  KEY `fk_book_has_book_catagories_book1_idx` (`ISBN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_has_book_categories`
--

LOCK TABLES `book_has_book_categories` WRITE;
/*!40000 ALTER TABLE `book_has_book_categories` DISABLE KEYS */;
INSERT INTO `book_has_book_categories` VALUES ('9781594633881',1),('9781594633881',3),('9781594633881',4),('9780307958198',12),('9781250126627',17);
/*!40000 ALTER TABLE `book_has_book_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `card`
--

DROP TABLE IF EXISTS `card`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `card` (
  `cardID` int NOT NULL,
  `cardNumber` varchar(45) DEFAULT NULL,
  `cardExpDate` datetime DEFAULT NULL COMMENT 'Only Month and Year fields are relevant for records.',
  `cardType` varchar(45) DEFAULT NULL,
  `cardSVC` int DEFAULT NULL,
  PRIMARY KEY (`cardID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `card`
--

LOCK TABLES `card` WRITE;
/*!40000 ALTER TABLE `card` DISABLE KEYS */;
INSERT INTO `card` VALUES (1001,'1001 1002 1003 1004',NULL,'MasterCard',NULL),(1002,'1234 5678 9012 3456',NULL,'Visa',NULL);
/*!40000 ALTER TABLE `card` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order` (
  `orderID` int NOT NULL,
  `orderTime` datetime DEFAULT NULL,
  `orderStatus` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'Either Pending, Placed, Shipped, or Arrived.',
  `orderAmount` double DEFAULT NULL,
  `promoID` int DEFAULT NULL,
  `addressID` int NOT NULL,
  `cardID` int NOT NULL,
  `userID` int NOT NULL,
  PRIMARY KEY (`orderID`),
  KEY `fk_order_promotion1_idx` (`promoID`),
  KEY `fk_order_address1_idx` (`addressID`),
  KEY `fk_order_card1_idx` (`cardID`),
  KEY `fk_order_users1_idx` (`userID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_has_book`
--

DROP TABLE IF EXISTS `order_has_book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_has_book` (
  `orderID` int NOT NULL,
  `ISBN` char(13) NOT NULL,
  `orderBookQuantity` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'Number of copies of the book ordered.',
  PRIMARY KEY (`orderID`,`ISBN`),
  KEY `fk_order_has_book_book1_idx` (`ISBN`),
  KEY `fk_order_has_book_order1_idx` (`orderID`),
  CONSTRAINT `fk_order_has_book_book1` FOREIGN KEY (`ISBN`) REFERENCES `book` (`ISBN`),
  CONSTRAINT `fk_order_has_book_order1` FOREIGN KEY (`orderID`) REFERENCES `order` (`orderID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_has_book`
--

LOCK TABLES `order_has_book` WRITE;
/*!40000 ALTER TABLE `order_has_book` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_has_book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promotion`
--

DROP TABLE IF EXISTS `promotion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `promotion` (
  `promoID` int NOT NULL,
  `promoDiscount` double DEFAULT NULL,
  `promoStart` datetime DEFAULT NULL,
  `promoEnd` datetime DEFAULT NULL,
  `promoEmailStatus` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'Either Emailed or Not Sent.',
  `promoUses` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'Keeps track of how many times a promotion was used.',
  PRIMARY KEY (`promoID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promotion`
--

LOCK TABLES `promotion` WRITE;
/*!40000 ALTER TABLE `promotion` DISABLE KEYS */;
INSERT INTO `promotion` VALUES (1,0.25,'2021-01-22 00:00:00','2021-04-22 00:00:00','Emailed','7'),(2,0.14,'2021-03-15 00:00:00','2021-03-30 00:00:00','Not Sent','0');
/*!40000 ALTER TABLE `promotion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shopping_cart`
--

DROP TABLE IF EXISTS `shopping_cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shopping_cart` (
  `cartID` int NOT NULL,
  `userID` int NOT NULL,
  PRIMARY KEY (`cartID`,`userID`),
  KEY `fk_shopping_cart_users1_idx` (`userID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shopping_cart`
--

LOCK TABLES `shopping_cart` WRITE;
/*!40000 ALTER TABLE `shopping_cart` DISABLE KEYS */;
INSERT INTO `shopping_cart` VALUES (1001,101),(1002,102),(1003,104),(1004,105),(1005,106),(1006,107);
/*!40000 ALTER TABLE `shopping_cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shopping_cart_has_book`
--

DROP TABLE IF EXISTS `shopping_cart_has_book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shopping_cart_has_book` (
  `cartID` int NOT NULL,
  `ISBN` char(13) NOT NULL,
  `cartBookQuantity` int DEFAULT NULL,
  PRIMARY KEY (`cartID`,`ISBN`),
  KEY `fk_shopping_cart_has_book_book1_idx` (`ISBN`),
  KEY `fk_shopping_cart_has_book_shopping_cart1_idx` (`cartID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shopping_cart_has_book`
--

LOCK TABLES `shopping_cart_has_book` WRITE;
/*!40000 ALTER TABLE `shopping_cart_has_book` DISABLE KEYS */;
/*!40000 ALTER TABLE `shopping_cart_has_book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `userID` int NOT NULL COMMENT 'Identifies Web Users, Admins, and Customers.',
  `userEmail` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'Needs to be unique for non-web users.',
  `userFName` varchar(45) DEFAULT NULL,
  `userLName` varchar(45) DEFAULT NULL,
  `userStatus` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'Either Active, Inactive, or Suspended.',
  `userType` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'Either Web User, Customer, or Admin.',
  `userPassword` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `addressID` int DEFAULT NULL COMMENT 'Can be null to account for the optional address field.',
  PRIMARY KEY (`userID`),
  UNIQUE KEY `userEmail_UNIQUE` (`userEmail`),
  KEY `fk_users_address1_idx` (`addressID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (101,'janedoe@gmail.com','Jane','Doe','Active','Customer','JaneDoe&22',101),(102,'johndoe@gmail.com','John','Doe','Active','Customer','JDoe42$**',101),(103,'jimmycricket@uga.edu','Jimmy','Cricket','Active','Admin','1234password!',NULL),(104,'petergriffin@yahoo.com','Peter','Griffin','Suspended','Customer','Loishehe54@',104),(105,NULL,NULL,NULL,NULL,'Web User',NULL,NULL),(106,'johnsnow@gmail.com','John','Snow','Inactive','Customer','asdf987#',NULL),(107,'lebronjames@yahoo.com','Lebron','James','Active','Customer','bBall4^LA',103);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_has_card`
--

DROP TABLE IF EXISTS `users_has_card`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_has_card` (
  `userEmail` varchar(45) NOT NULL,
  `cardID` int NOT NULL,
  PRIMARY KEY (`userEmail`,`cardID`),
  KEY `fk_users_has_card_card1_idx` (`cardID`),
  KEY `fk_users_has_card_users_idx` (`userEmail`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_has_card`
--

LOCK TABLES `users_has_card` WRITE;
/*!40000 ALTER TABLE `users_has_card` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_has_card` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-22 15:26:35
