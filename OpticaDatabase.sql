-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 29, 2022 at 06:22 PM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `optitplus`
--

-- --------------------------------------------------------

--
-- Table structure for table `cliente`
--

DROP IF EXISTS DATABASE optitplus;
CREATE DATABASE optiplus;
use optiplus;

CREATE TABLE `cliente` (
  `id` mediumint(9) NOT NULL,
  `nombre` char(30) NOT NULL,
  `cedula` int(31) NOT NULL,
  `genero` char(1) NOT NULL,
  `celular` int(31) NOT NULL,
  `fechaNacimiento` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cliente`
--

INSERT INTO `cliente` (`id`, `nombre`, `cedula`, `genero`, `celular`, `fechaNacimiento`) VALUES
(1, '21', 121, 'm', 12312, '2022-11-08'),
(2, '21', 1211, 'm', 12312, '2022-11-08'),
(3, 'prueba', 1234, 'm', 12312, '2022-11-08'),
(4, 'juan', 12345, 'm', 122334, '2022-11-01');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `cedula` mediumint(9) NOT NULL,
  `password` varchar(256) NOT NULL,
  `admin` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`cedula`, `password`, `admin`) VALUES
(1211, 'sha256$jVpakNib1RCPgiE5$b23cb4cc5a346cb8063ec2978f8bfa1852e1381ba5edafed8875421aae1f1c38', NULL),
(1234, 'sha256$wzftXaz1dmPnTjt1$2f4f1553c0eaec1251cd30af2dfc00ce310858ee1ae6d4338316178db9a9b92b', 1),
(12345, 'sha256$p6096b8tuyTB91Xm$627d2d0779f32376e620401e333038ab3001215798ea37c2c3cef422eeeaac75', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `pedido`
--

CREATE TABLE `pedido` (
  `idPedido` mediumint(9) NOT NULL,
  `idCliente` mediumint(9) NOT NULL,
  `cantidad` int(31) NOT NULL,
  `total` int(31) NOT NULL,
  `estado` char(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `producto`
--

CREATE TABLE `producto` (
  `idProducto` mediumint(9) NOT NULL,
  `nombre` char(30) NOT NULL,
  `descripcion` char(200) NOT NULL,
  `precioVenta` int(31) NOT NULL,
  `precioCompra` int(31) NOT NULL,
  `existencias` int(31) NOT NULL,
  `image` varchar(200) DEFAULT NULL,
  `categoria` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `producto`
--

INSERT INTO `producto` (`idProducto`, `nombre`, `descripcion`, `precioVenta`, `precioCompra`, `existencias`, `image`, `categoria`) VALUES
(2, 'DOWEL', 'Material: Acetato, TR90\n\nColores: Negro, Azul', 58, 58, 100, '/static/images/montura-2.png', 'monturas'),
(4, 'Heart pupil', 'Heart pupil', 50, 50, 50, '/static/images/menu-1.png', 'contactos'),
(5, 'Gris fantasia', 'Gris fantasia', 50, 50, 50, '/static/images/menu-2.png', 'contactos'),
(6, 'tasty and healty', 'tasty and healty', 50, 50, 50, '/static/images/menu-3.png', 'contactos'),
(7, 'Azul brillante', 'Azul brillante', 50, 50, 50, '/static/images/menu-4.png', 'contactos'),
(8, 'Safiro', 'Safiro', 50, 50, 50, '/static/images/menu-5.png', 'contactos'),
(9, 'Gris claro', 'Gris claro', 50, 50, 50, '/static/images/menu-6.png', 'contactos'),
(10, 'CHARLING', 'CHARLING', 80, 80, 150, '/static/images/product-1.png', 'sol'),
(11, 'AFRICA', 'AFRICA', 80, 80, 150, '/static/images/product-2.png', 'sol'),
(12, 'Beili', 'Beili', 80, 80, 150, '/static/images/product-3.png', 'sol'),
(13, 'CUBIK', 'Material: Acetato, TR90, Pasta \n Colores: Rosado, Verde, Azul', 100, 100, 20, '/static/images/montura-1.png', 'monturas'),
(14, 'DAKOTA', 'Material: TR90 \n Colores: Negro, Naranja', 100, 100, 20, '/static/images/montura-3.png', 'monturas');

-- --------------------------------------------------------

--
-- Table structure for table `venta`
--

CREATE TABLE `venta` (
  `idVenta` mediumint(9) NOT NULL,
  `idCliente` mediumint(9) NOT NULL,
  `descuento` int(31) NOT NULL,
  `total` int(31) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`cedula`,`password`);

--
-- Indexes for table `pedido`
--
ALTER TABLE `pedido`
  ADD PRIMARY KEY (`idPedido`),
  ADD KEY `idCliente` (`idCliente`);

--
-- Indexes for table `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`idProducto`);

--
-- Indexes for table `venta`
--
ALTER TABLE `venta`
  ADD PRIMARY KEY (`idVenta`),
  ADD KEY `idCliente` (`idCliente`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cliente`
--
ALTER TABLE `cliente`
  MODIFY `id` mediumint(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `pedido`
--
ALTER TABLE `pedido`
  MODIFY `idPedido` mediumint(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `producto`
--
ALTER TABLE `producto`
  MODIFY `idProducto` mediumint(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `pedido`
--
ALTER TABLE `pedido`
  ADD CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`idCliente`) REFERENCES `cliente` (`id`);

--
-- Constraints for table `venta`
--
ALTER TABLE `venta`
  ADD CONSTRAINT `venta_ibfk_1` FOREIGN KEY (`idCliente`) REFERENCES `cliente` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
