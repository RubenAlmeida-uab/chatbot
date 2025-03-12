-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: uab_dashboard
-- ------------------------------------------------------
-- Server version	9.0.1

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
-- Table structure for table `comandos_pesquisados`
--

DROP TABLE IF EXISTS `comandos_pesquisados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comandos_pesquisados` (
  `id_comando` int NOT NULL AUTO_INCREMENT,
  `comando` varchar(255) NOT NULL,
  `categoria` varchar(100) NOT NULL,
  `num_pesquisas` int NOT NULL DEFAULT '0',
  `ultima_pesquisa` datetime NOT NULL,
  PRIMARY KEY (`id_comando`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comandos_pesquisados`
--

LOCK TABLES `comandos_pesquisados` WRITE;
/*!40000 ALTER TABLE `comandos_pesquisados` DISABLE KEYS */;
INSERT INTO `comandos_pesquisados` VALUES (1,'como acessar notas','Acadêmico',150,'2025-03-10 21:20:00'),(2,'login na plataforma','Acesso',90,'2025-03-11 14:05:00'),(3,'alterar senha','Configuração',120,'2025-03-12 09:30:00'),(4,'horários das aulas','Acadêmico',80,'2025-03-10 08:45:00'),(5,'materiais de estudo','Recursos',200,'2025-03-12 18:15:00');
/*!40000 ALTER TABLE `comandos_pesquisados` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-12 21:54:46
