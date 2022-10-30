-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: grocart
-- ------------------------------------------------------
-- Server version	8.0.30

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
-- Dumping data for table `cart`
--
use grocart;

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
INSERT INTO `cart` VALUES (1,202212002,1,'4.340 g');
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'bracelets_bangles','2022-10-17 20:20:56'),(2,'earrings','2022-10-17 20:20:56'),(3,'mangalsutras','2022-10-17 20:20:56'),(4,'necklaces','2022-10-17 20:20:56'),(5,'other_jewellery','2022-10-17 20:20:56'),(6,'pendants','2022-10-17 20:20:56'),(7,'rings','2022-10-17 20:20:56');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` VALUES (2,'2022-03-13 17:34:02',48,1),(3,'2022-03-13 17:46:53',16,2),(4,'2022-03-13 17:50:50',16,2),(5,'2022-03-14 21:38:45',64,2),(6,'2022-03-14 21:53:53',16,2),(7,'2022-03-14 22:00:07',16,2),(8,'2022-03-14 22:04:04',16,2),(9,'2022-03-15 05:59:01',16,2),(10,'2022-03-20 07:23:04',16,1),(11,'2022-03-21 15:15:54',1924,1),(12,'2022-03-21 15:16:29',1924,1),(13,'2022-03-21 15:18:06',1924,1),(14,'2022-03-21 15:19:51',869,2),(15,'2022-03-21 15:21:28',869,2),(16,'2022-03-24 11:59:04',7955,1),(17,'2022-10-17 12:06:56',869,1),(18,'2022-10-17 12:13:01',869,1),(19,'2022-10-17 12:15:29',869,1),(20,'2022-10-17 12:16:48',869,1),(21,'2022-10-17 12:18:00',869,1),(22,'2022-10-17 12:20:06',869,1),(23,'2022-10-17 12:21:29',869,1),(24,'2022-10-17 12:21:57',869,1),(25,'2022-10-17 13:35:43',3444,1),(26,'2022-10-17 17:13:22',9842,1);
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ordered_details`
--

LOCK TABLES `ordered_details` WRITE;
/*!40000 ALTER TABLE `ordered_details` DISABLE KEYS */;
INSERT INTO `ordered_details` VALUES (1,26,202212002,1,'1.220 g ');
/*!40000 ALTER TABLE `ordered_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (202212001,1,'UT00815-YG0000','Swastik Baby Nazaria Gold Bracelet Set of 2','Set in 18 KT Yellow Gold(2.010 g)','https://cdn.caratlane.com/media/catalog/product/cache/6/image/480x480/9df78eab33525d08d6e5fb8d27136e95//U/T/UT00815-YG0000_11_listfront.jpg',100,13233,12030,5,NULL,'bracelets_bangles','Caratlane','2.010 g'),(202212002,1,'JT00216-YGP600','Amra Crown Kids\' Diamond Bracelet','\'Set in 18 KT Yellow Gold(1.360 g) with diamonds (0.040 ct ,GH-SI)\'','https://cdn.caratlane.com/media/catalog/product/cache/6/image/480x480/9df78eab33525d08d6e5fb8d27136e95//J/T/JT00216-YGP600_11_listfront.jpg',100,15571,14155,5,NULL,'bracelets_bangles','Caratlane','1.360 g'),(202212003,2,'UT00709-1Y0000','Sana Mangalsutra Gold Bracelet','Set in 14 KT Yellow Gold(1.770 g)','https://cdn.caratlane.com/media/catalog/product/cache/6/image/480x480/9df78eab33525d08d6e5fb8d27136e95//U/T/UT00709-1Y0000_11_listfront.jpg',100,11600,10545,5,NULL,'bracelets_bangles','Caratlane','1.770 g'),(202212004,2,'JT00920-1RP600','Floria Diamond Bracelet','\'Set in 14 KT Rose Gold(1.300 g) with diamonds (0.079 ct ,GH-SI)\'','https://cdn.caratlane.com/media/catalog/product/cache/6/image/480x480/9df78eab33525d08d6e5fb8d27136e95//J/T/JT00920-1RP600_11_listfront.jpg',100,17579,15981,5,NULL,'bracelets_bangles','Caratlane','1.300 g'),(202212005,1,'JE04645-YGP900','Caratlane','\'Set in 18 KT Yellow Gold(5.200 g) with diamonds (0.200 ct ,IJ-SI)\'','https://cdn.caratlane.com/media/catalog/product/cache/6/image/480x480/9df78eab33525d08d6e5fb8d27136e95//J/E/JE04645-YGP600_11_listfront.jpg',100,58301,53001,5,NULL,'earrings','Caratlane','5.200 g'),(202212006,1,'JE04067-YGP9RS','Caratlane','\'Set in 18 KT Yellow Gold(5.440 g) with diamonds (0.160 ct ,IJ-SI)\'','https://cdn.caratlane.com/media/catalog/product/cache/6/image/480x480/9df78eab33525d08d6e5fb8d27136e95//J/E/JE04067-YGP9RS_11_listfront.jpg',100,57200,52000,5,NULL,'earrings','Caratlane','5.440 g'),(202212007,2,'JE04813-RGP9SS','Caratlane','\'Set in 18 KT Rose Gold(2.940 g) with diamonds (0.360 ct ,IJ-SI)\'','https://cdn.caratlane.com/media/catalog/product/cache/6/image/480x480/9df78eab33525d08d6e5fb8d27136e95//J/E/JE04813-RGP9SS_11_listfront.jpg',100,68129,61935,5,NULL,'earrings','Caratlane','2.940 g'),(202212008,2,'JE02449-YGP900','Caratlane','\'Set in 18 KT Yellow Gold(3.140 g) with diamonds (0.540 ct ,IJ-SI)\'','https://cdn.caratlane.com/media/catalog/product/cache/6/image/480x480/9df78eab33525d08d6e5fb8d27136e95//J/E/JE02449-YGP600_11_listfront.jpg',100,73802,67093,5,NULL,'earrings','Caratlane','3.140 g');
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `product_category`
--

LOCK TABLES `product_category` WRITE;
/*!40000 ALTER TABLE `product_category` DISABLE KEYS */;
INSERT INTO `product_category` VALUES (1,1,202212001,1,'2022-10-17 22:18:02'),(2,1,202212002,1,'2022-10-17 22:18:02'),(3,1,202212003,2,'2022-10-17 22:18:02'),(4,1,202212004,2,'2022-10-17 22:18:02'),(5,2,202212005,1,'2022-10-17 22:18:02'),(6,2,202212006,1,'2022-10-17 22:18:02'),(7,2,202212007,2,'2022-10-17 22:18:02'),(8,2,202212008,2,'2022-10-17 22:18:02');
/*!40000 ALTER TABLE `product_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `sale_transaction`
--

LOCK TABLES `sale_transaction` WRITE;
/*!40000 ALTER TABLE `sale_transaction` DISABLE KEYS */;
INSERT INTO `sale_transaction` VALUES (1,13,'2022-03-21 00:00:00',1924,'1111111111111134','amex','success'),(2,14,'2022-03-21 00:00:00',869,'1111111111111234','amex','success'),(3,15,'2022-03-21 00:00:00',869,'1111111111111234','amex','success'),(4,16,'2022-03-24 00:00:00',7955,'1111111111111111','mastercard','success'),(5,23,'2022-10-17 12:21:29',869,'1234567812345678','visa','success'),(6,24,'2022-10-17 12:21:57',869,'1234567812345678','visa','success'),(7,25,'2022-10-17 13:35:43',3444,'1234567812345678','visa','success'),(8,26,'2022-10-17 17:13:22',9842,'1234567812345678','visa','success');
/*!40000 ALTER TABLE `sale_transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `sub_products`
--

LOCK TABLES `sub_products` WRITE;
/*!40000 ALTER TABLE `sub_products` DISABLE KEYS */;
/*!40000 ALTER TABLE `sub_products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Sravan','Voona','cd84d683cc5612c69efe115c80d0b7dc','Vishakapatnam','Visakhapatnam','Andhra Pradesh','India','530041','sras1729@gmail.com','1111111111','startup','ASDFG1234Q','145236521254',0,1,1);
INSERT INTO `user` VALUES (2,'Deepak','Hooda','cd84d683cc5612c69efe115c80d0b7dc','Vishakapatnam','Visakhapatnam','Andhra Pradesh','India','530041','sras1729@gmail.com','1111111101','nbfc','ASDFG1234F','145236524562',0,1,1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-10-18 17:07:50
