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
  `addressZip` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`addressID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address`
--

LOCK TABLES `address` WRITE;
/*!40000 ALTER TABLE `address` DISABLE KEYS */;
INSERT INTO `address` VALUES (101,'H Street','Brunswick','TN','30754'),(102,'245 Mario Lane','San Francisco','CA','01458'),(103,'987 Sunset Boulevard','Los Angeles','CA','16542'),(104,'221 Baked Alaska Way','Miami','FL','98754'),(105,'4741 Angel Road','Flowery Branch','GA','21252');
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
  `bookImage` varchar(50) DEFAULT NULL,
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
INSERT INTO `book` VALUES ('9780063012196','The Divines','Ellie','Eaton','the divines.jpg',20.39,11,4,'William Morrow','2021-01-19 00:00:00','Phasellus non libero id tortor ultrices pellentesque non sit amet odio. Aliquam augue purus, gravida a enim non, laoreet feugiat enim. Donec vestibulum odio quam, sed ullamcorper dolor aliquam sed. Nunc id magna congue diam elementum tincidunt. Sed pulvinar eros magna, id cursus justo iaculis eu. Nunc eleifend magna libero, eu tempor odio pellentesque id. Mauris lobortis iaculis rutrum. Vestibulum eu mi condimentum, bibendum massa eu, bibendum leo. Aenean porta dui id maximus vehicula. Etiam id suscipit risus. '),('9780307958198','Black Hole Blues and Other Songs from Outer Space','Janna','Levin','black hole blues.jpg',22.19,7,4,'Knopf','2016-03-29 00:00:00','Nunc non ante tellus. Morbi vitae maximus libero, eu sagittis leo. Vestibulum eu nisl feugiat, dapibus ante a, ultricies diam. Vivamus aliquet accumsan blandit. Sed elementum nibh elit, ullamcorper rhoncus nulla molestie sit amet. Sed justo tellus, lacinia nec urna pretium, fringilla dapibus leo. Phasellus rhoncus nibh ligula, sed tincidunt velit venenatis id. Praesent condimentum neque vel efficitur ultrices. Praesent vitae placerat elit. Quisque a mattis ex. Vestibulum volutpat velit quis purus ullamcorper elementum. '),('9780385537674','Fifty Shades of Grey','Erika','Leonard','fifty shades.jpg',26.95,13,4,'Doubleday','2013-01-29 00:00:00','Vestibulum ullamcorper massa mattis, lacinia neque eu, rutrum dui. Maecenas sodales semper vestibulum. Donec ultrices turpis vitae orci bibendum, ac fringilla ante commodo. Etiam justo neque, posuere nec vulputate ut, luctus sit amet augue. Nam aliquam ante eu ipsum porta porta. Pellentesque a dolor eu leo sollicitudin consequat sed a nibh. Quisque aliquet orci eu vulputate cursus. Suspendisse eu malesuada lectus, sed aliquam nisi. Aenean tempus ligula vel mollis hendrerit. Duis in libero tincidunt, consequat neque non, sagittis ex. Morbi finibus consectetur lectus in semper. Donec mollis est id erat imperdiet euismod. '),('9780451493095','All We Saw','Anne','Michaels','all we saw.jpg',17.99,14,5,'Knopf','2017-10-03 00:00:00','In iaculis dolor ac ligula porttitor, in dignissim ex lacinia. Sed id enim sit amet urna fringilla ullamcorper tristique ut libero. Duis faucibus sollicitudin erat at molestie. Donec in finibus tellus, eget luctus magna. Morbi quis ornare libero. Phasellus sapien sem, sodales sed hendrerit non, fermentum sit amet ex. Proin pellentesque lectus et auctor interdum. In vulputate ligula sodales felis tristique, nec aliquam nibh mattis. Maecenas eu neque gravida, consequat ipsum sed, dignissim est. Vivamus efficitur nibh at lectus pellentesque sollicitudin. Cras varius est laoreet, ornare ipsum et, faucibus felis. In ac condimentum ligula, vel bibendum dui. Nunc ultricies mattis enim, et ultricies augue tempor a. Cras placerat risus odio, non porttitor nisi fringilla sed. Sed quis efficitur tellus, eget tincidunt dolor.'),('9780593311684','The Cheffe: A Cook\'s Novel','Marie','NDiaye','cheffe.jpg',22.99,15,4,'Vintage','2021-01-19 00:00:00','Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam nec nisi metus. Duis egestas purus a justo mattis sodales. In hac habitasse platea dictumst. Vivamus lorem leo, sodales vel quam eu, elementum ullamcorper nunc. Morbi ligula arcu, lobortis eget convallis vel, tristique ut diam. Nulla at magna elit. Etiam vel ultrices purus. '),('9781101994979','That Inevitable Victorian Thing','Emily','Johnston','inevitable victorian thing.jpg',8.99,20,3,'Dutton Books for Young Readers','2017-10-03 00:00:00','Donec varius tincidunt ante fringilla eleifend. Phasellus lacinia convallis nunc, hendrerit ullamcorper est tincidunt eu. Nam a dignissim massa. Donec viverra arcu at est scelerisque interdum. Curabitur suscipit a ante id vestibulum. Nam pellentesque iaculis dictum. Nam auctor orci vitae ligula volutpat, ut tincidunt dui volutpat. Sed congue mi viverra sollicitudin consequat. Etiam semper consequat egestas. Donec lobortis ultrices leo sed malesuada. Integer ac tincidunt enim, eget pretium tellus. Morbi laoreet porttitor ipsum vel mattis. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nulla luctus lacus tortor, a blandit nisl mollis eu. Vestibulum ligula ligula, porta et malesuada sit amet, finibus viverra mi. Vestibulum accumsan purus neque, quis iaculis turpis maximus in'),('9781250126627','A Selfie as Big as the Ritz','Lara','Williams','selfie as big as the ritz.jpg',9.95,4,4,'Flatiron Books','2017-10-31 00:00:00','Aenean egestas diam et porta vulputate. Curabitur ac sem tincidunt quam placerat ultricies vitae a justo. Etiam tempus leo ut erat pharetra pellentesque. Nam a lacus nulla. Nam eu luctus odio. Etiam et ante a velit porta tempor et tristique metus. Nunc scelerisque mi quis neque vulputate aliquam. Donec rhoncus quam sit amet erat facilisis, sit amet porttitor erat porttitor. Curabitur condimentum, ligula et vulputate accumsan, mauris nunc tincidunt ipsum, vel semper odio est at nunc. Etiam sagittis laoreet tellus in pretium. Curabitur quis turpis vitae erat sodales iaculis aliquet eget eros. '),('9781594625459','Voices in the Night','Steven','Millhauser','voices in the night.jpg',15.99,12,4,'Kipster Books','2012-11-22 00:00:00','Praesent augue mi, efficitur ut nulla vitae, consectetur aliquet ex. Sed mattis eget est in porta. Integer eu volutpat quam. Aliquam dapibus ex vulputate imperdiet rutrum. Proin dapibus venenatis massa, a imperdiet enim ullamcorper id. Nunc ultricies vel dui eget efficitur. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Donec purus urna, tristique at sodales quis, tempor at enim. Nulla purus metus, convallis et neque et, egestas dictum nulla. Mauris euismod purus sed mattis ultrices. '),('9781594633881','The Vacationers','Emma','Straub','the vacationers.jpg',25.99,9,3,'Penguin Publishing Group','2014-06-02 00:00:00','For the Posts, a two-week trip to the Balearic island of Mallorca with their extended family and friends is a celebration: Franny and Jim are observing their thirty-fifth wedding anniversary, and their daughter, Sylvia, has graduated from high school. The sunlit island, its mountains and beaches, its tapas and tennis courts, also promise an escape from the tensions simmering at home in Manhattan. But all does not go according to plan: over the course of the vacation, secrets come to light, old and new humiliations are experienced, childhood rivalries resurface, and ancient wounds are exacerbated.'),('9781594634109','Hiding in Plain Sight','Nuruddin','Farah','nuruddin farah.jpg',18.99,5,3,'Riverhead Books','2015-09-22 00:00:00','Nulla vel mauris sit amet justo consequat auctor eu a ex. Phasellus non lacinia mauris. Phasellus nec leo in ipsum sodales malesuada at a metus. Morbi vestibulum arcu orci, a rutrum mi cursus a. Fusce eget nibh ut neque volutpat rutrum. In cursus non nibh vitae posuere. Cras fermentum diam ac diam tincidunt, eget elementum risus ultricies. ');
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
INSERT INTO `book_categories` VALUES (1,'Featured'),(2,'Education'),(3,'Domestic Fiction'),(4,'Drama'),(5,'Classic'),(6,'Thriller'),(7,'Romance'),(8,'History'),(9,'Young Adult'),(10,'Esoteric'),(11,'Science Fiction'),(12,'Science'),(13,'Self-Help'),(14,'Non-Fiction'),(15,'Horror'),(16,'Business'),(17,'Short Stories'),(18,'Newly Released');
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
INSERT INTO `book_has_book_categories` VALUES ('9780063012196',1),('9780385537674',1),('9780593311684',1),('9781594633881',1),('9781594633881',3),('9781594633881',4),('9781594625459',6),('9781594625459',7),('9781594625459',8),('9780307958198',12),('9781250126627',17),('9780307958198',18),('9781250126627',18),('9781594625459',18),('9781594634109',18);
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
INSERT INTO `card` VALUES (1001,'0101 6969 8787 1111','2028-06-01 00:00:00','Visa',221),(1002,'1234 5678 9012 3456',NULL,'Visa',NULL),(1003,'8989 7474 5656 0000',NULL,'MasterCard',100),(1004,'1111 1111 1111 0000',NULL,'Discover',777),(1005,'7777 4444 0125 3210','2030-12-01 00:00:00','MasterCard',123);
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
  `userPhone` varchar(45) DEFAULT NULL,
  `userSubStatus` varchar(45) DEFAULT NULL,
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
INSERT INTO `users` VALUES (101,'janedoe@gmail.com','Jennifer','Jones','Active','Customer','password','123-456-2558','Deactive',105),(102,'johndoe@gmail.com','John','Doe','Active','Customer','JDoe42$**','971-221-8787','Active',101),(103,'jimmycricket@uga.edu','Jimmy','Cricket','Active','Admin','1234password!','124-458-9989','Deactive',NULL),(104,'petergriffin@yahoo.com','Peter','Griffin','Suspended','Customer','Loishehe54@','245-545-7777','Deactive',104),(105,NULL,NULL,NULL,NULL,'Web User',NULL,NULL,NULL,NULL),(106,'johnsnow@gmail.com','John','Snow','Inactive','Customer','asdf987#','656-221-6240','Deactive',NULL),(107,'lebronjames@yahoo.com','Lebron','James','Active','Customer','bBall4^LA','987-145-6654','Active',103);
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
INSERT INTO `users_has_card` VALUES ('janedoe@gmail.com',1001);
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

-- Dump completed on 2021-03-30 13:45:57
