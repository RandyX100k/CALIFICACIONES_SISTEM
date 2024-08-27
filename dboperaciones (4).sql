-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-05-2023 a las 02:02:09
-- Versión del servidor: 10.4.27-MariaDB
-- Versión de PHP: 8.0.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `dboperaciones`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alumnos`
--

CREATE TABLE `alumnos` (
  `ID` int(11) NOT NULL,
  `Nombre_Completo` varchar(100) NOT NULL,
  `Curso` varchar(100) NOT NULL,
  `Email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

--
-- Volcado de datos para la tabla `alumnos`
--

INSERT INTO `alumnos` (`ID`, `Nombre_Completo`, `Curso`, `Email`) VALUES
(35, 'Maria A', '5T0F-01', 'malejandrina035@gmail.com'),
(36, 'Starling ', '5T0F-01', 'ml20271411@gmail.com'),
(37, 'Joel Gonzalez', '5TOF-02', 'neonexem@gmail.com'),
(38, 'Kiko pedro', '5TOF-02', 'joelrandy86@gmail.com'),
(39, 'Jose Rijo', '5TOF-02', 'joserijo81@gmail.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `calificaciones`
--

CREATE TABLE `calificaciones` (
  `ID` int(11) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Curso` varchar(100) NOT NULL,
  `Materia` varchar(100) NOT NULL,
  `RA1` varchar(100) NOT NULL,
  `RA2` varchar(100) NOT NULL,
  `RA3` varchar(100) NOT NULL,
  `RA4` varchar(100) NOT NULL,
  `RA5` varchar(100) NOT NULL,
  `RA6` varchar(100) NOT NULL,
  `RA7` varchar(100) NOT NULL,
  `RA8` varchar(100) NOT NULL,
  `RA9` varchar(100) NOT NULL,
  `RA10` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

--
-- Volcado de datos para la tabla `calificaciones`
--

INSERT INTO `calificaciones` (`ID`, `Nombre`, `Curso`, `Materia`, `RA1`, `RA2`, `RA3`, `RA4`, `RA5`, `RA6`, `RA7`, `RA8`, `RA9`, `RA10`) VALUES
(116, 'Joel Gonzalez', '5T0F-01', 'Administracion de bases de datos', '1', '', '', '', '', '', '', '', '', ''),
(117, 'Maria A', '5T0F-01', 'Administracion de bases de datos', '31', '', '', '', '', '', '', '', '', ''),
(118, 'Kiko pedro', '5T0F-01', 'Administracion de bases de datos', '0', '', '', '', '', '', '', '', '', ''),
(119, 'Starling ', '5T0F-01', 'Administracion de bases de datos', '0', '', '', '', '', '', '', '', '', ''),
(120, 'Jose Rijo', '5T0F-01', 'Administracion de bases de datos', '0', '', '', '', '', '', '', '', '', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cursos`
--

CREATE TABLE `cursos` (
  `ID` int(11) NOT NULL,
  `Curso` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

--
-- Volcado de datos para la tabla `cursos`
--

INSERT INTO `cursos` (`ID`, `Curso`) VALUES
(1, '5T0F-01'),
(5, '5TOF-02'),
(3, '6TO-F');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `materias`
--

CREATE TABLE `materias` (
  `ID` int(11) NOT NULL,
  `Materia` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

--
-- Volcado de datos para la tabla `materias`
--

INSERT INTO `materias` (`ID`, `Materia`) VALUES
(2, 'Administracion de bases de datos'),
(3, 'Desarrollo de aplicaciones');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `quejas`
--

CREATE TABLE `quejas` (
  `ID` int(11) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `queja` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ra1`
--

CREATE TABLE `ra1` (
  `ID` int(11) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Materia` varchar(100) NOT NULL,
  `Curso` varchar(100) NOT NULL,
  `Asistencia` varchar(100) NOT NULL,
  `P1` varchar(100) NOT NULL,
  `P2` varchar(100) NOT NULL,
  `P3` varchar(100) NOT NULL,
  `P4` varchar(100) NOT NULL,
  `P5` varchar(100) NOT NULL,
  `Cuaderno` varchar(100) NOT NULL,
  `Total` varchar(100) NOT NULL,
  `M1` varchar(100) NOT NULL,
  `M2` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

--
-- Volcado de datos para la tabla `ra1`
--

INSERT INTO `ra1` (`ID`, `Nombre`, `Materia`, `Curso`, `Asistencia`, `P1`, `P2`, `P3`, `P4`, `P5`, `Cuaderno`, `Total`, `M1`, `M2`) VALUES
(102, 'Joel Gonzalez', 'Administracion de bases de datos', '5T0F-01', '1', '0', '0', '0', '0', '0', '0', '1', '2', '2'),
(103, 'Maria A', 'Administracion de bases de datos', '5T0F-01', '10', '8', '3', '2', '8', '0', '5', '31', '0', '0'),
(104, 'Kiko pedro', 'Administracion de bases de datos', '5T0F-01', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
(105, 'Starling ', 'Administracion de bases de datos', '5T0F-01', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
(106, 'Jose Rijo', 'Administracion de bases de datos', '5T0F-01', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ra2`
--

CREATE TABLE `ra2` (
  `ID` int(11) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Materia` varchar(100) NOT NULL,
  `Curso` varchar(100) NOT NULL,
  `Asistencia` varchar(100) NOT NULL,
  `P1` varchar(100) NOT NULL,
  `P2` varchar(100) NOT NULL,
  `P3` varchar(100) NOT NULL,
  `P4` varchar(100) NOT NULL,
  `P5` varchar(100) NOT NULL,
  `Cuaderno` varchar(100) NOT NULL,
  `Total` varchar(100) NOT NULL,
  `M1` varchar(100) NOT NULL,
  `M2` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ra3`
--

CREATE TABLE `ra3` (
  `ID` int(11) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Materia` varchar(100) NOT NULL,
  `Curso` varchar(100) NOT NULL,
  `Asistencia` varchar(100) NOT NULL,
  `P1` varchar(100) NOT NULL,
  `P2` varchar(100) NOT NULL,
  `P3` varchar(100) NOT NULL,
  `P4` varchar(100) NOT NULL,
  `P5` varchar(100) NOT NULL,
  `Cuaderno` varchar(100) NOT NULL,
  `Total` varchar(100) NOT NULL,
  `M1` varchar(100) NOT NULL,
  `M2` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ra4`
--

CREATE TABLE `ra4` (
  `ID` int(11) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Materia` varchar(100) NOT NULL,
  `Curso` varchar(100) NOT NULL,
  `Asistencia` varchar(100) NOT NULL,
  `P1` varchar(100) NOT NULL,
  `P2` varchar(100) NOT NULL,
  `P3` varchar(100) NOT NULL,
  `P4` varchar(100) NOT NULL,
  `P5` varchar(100) NOT NULL,
  `Cuaderno` varchar(100) NOT NULL,
  `Total` varchar(100) NOT NULL,
  `M1` varchar(100) NOT NULL,
  `M2` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ra5`
--

CREATE TABLE `ra5` (
  `ID` int(11) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Materia` varchar(100) NOT NULL,
  `Curso` varchar(100) NOT NULL,
  `Asistencia` varchar(100) NOT NULL,
  `P1` varchar(100) NOT NULL,
  `P2` varchar(100) NOT NULL,
  `P3` varchar(100) NOT NULL,
  `P4` varchar(100) NOT NULL,
  `P5` varchar(100) NOT NULL,
  `Cuaderno` varchar(100) NOT NULL,
  `Total` varchar(100) NOT NULL,
  `M1` varchar(100) NOT NULL,
  `M2` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ra6`
--

CREATE TABLE `ra6` (
  `ID` int(11) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Materia` varchar(100) NOT NULL,
  `Curso` varchar(100) NOT NULL,
  `Asistencia` varchar(100) NOT NULL,
  `P1` varchar(100) NOT NULL,
  `P2` varchar(100) NOT NULL,
  `P3` varchar(100) NOT NULL,
  `P4` varchar(100) NOT NULL,
  `P5` varchar(100) NOT NULL,
  `Cuaderno` varchar(100) NOT NULL,
  `Total` varchar(100) NOT NULL,
  `M1` varchar(100) NOT NULL,
  `M2` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ra7`
--

CREATE TABLE `ra7` (
  `ID` int(11) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Materia` varchar(100) NOT NULL,
  `Curso` varchar(100) NOT NULL,
  `Asistencia` varchar(100) NOT NULL,
  `P1` varchar(100) NOT NULL,
  `P2` varchar(100) NOT NULL,
  `P3` varchar(100) NOT NULL,
  `P4` varchar(100) NOT NULL,
  `P5` varchar(100) NOT NULL,
  `Cuaderno` varchar(100) NOT NULL,
  `Total` varchar(100) NOT NULL,
  `M1` varchar(100) NOT NULL,
  `M2` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ra8`
--

CREATE TABLE `ra8` (
  `ID` int(11) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Materia` varchar(100) NOT NULL,
  `Curso` varchar(100) NOT NULL,
  `Asistencia` varchar(100) NOT NULL,
  `P1` varchar(100) NOT NULL,
  `P2` varchar(100) NOT NULL,
  `P3` varchar(100) NOT NULL,
  `P4` varchar(100) NOT NULL,
  `P5` varchar(100) NOT NULL,
  `Cuaderno` varchar(100) NOT NULL,
  `Total` varchar(100) NOT NULL,
  `M1` varchar(100) NOT NULL,
  `M2` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ra9`
--

CREATE TABLE `ra9` (
  `ID` int(11) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Materia` varchar(100) NOT NULL,
  `Curso` varchar(100) NOT NULL,
  `Asistencia` varchar(100) NOT NULL,
  `P1` varchar(100) NOT NULL,
  `P2` varchar(100) NOT NULL,
  `P3` varchar(100) NOT NULL,
  `P4` varchar(100) NOT NULL,
  `P5` varchar(100) NOT NULL,
  `Cuaderno` varchar(100) NOT NULL,
  `Total` varchar(100) NOT NULL,
  `M1` varchar(100) NOT NULL,
  `M2` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ra10`
--

CREATE TABLE `ra10` (
  `ID` int(11) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Materia` varchar(100) NOT NULL,
  `Curso` varchar(100) NOT NULL,
  `Asistencia` varchar(100) NOT NULL,
  `P1` varchar(100) NOT NULL,
  `P2` varchar(100) NOT NULL,
  `P3` varchar(100) NOT NULL,
  `P4` varchar(100) NOT NULL,
  `P5` varchar(100) NOT NULL,
  `Cuaderno` varchar(100) NOT NULL,
  `Total` varchar(100) NOT NULL,
  `M1` varchar(100) NOT NULL,
  `M2` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

--
-- Volcado de datos para la tabla `ra10`
--

INSERT INTO `ra10` (`ID`, `Nombre`, `Materia`, `Curso`, `Asistencia`, `P1`, `P2`, `P3`, `P4`, `P5`, `Cuaderno`, `Total`, `M1`, `M2`) VALUES
(6, 'Starling ', 'Administracion de bases de datos', '5T0F-01', '1', '1', '1', '0', '0', '1', '0', '4', '', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `session`
--

CREATE TABLE `session` (
  `ID` int(11) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `IP` varchar(100) NOT NULL,
  `rol` varchar(100) NOT NULL,
  `Fecha` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

--
-- Volcado de datos para la tabla `session`
--

INSERT INTO `session` (`ID`, `Email`, `IP`, `rol`, `Fecha`) VALUES
(61, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-11'),
(62, 'joserijo81@gmail.com', '127.0.0.1', 'user', '2023-05-11'),
(63, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-11'),
(64, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-11'),
(65, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-11'),
(66, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-11'),
(67, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-11'),
(68, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-12'),
(69, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-13'),
(70, 'ml20271411@gmail.com', '127.0.0.1', 'user', '2023-05-13'),
(71, 'neonexem@gmail.com', '127.0.0.1', 'user', '2023-05-13'),
(72, 'joelrandy86@gmail.com', '127.0.0.1', 'user', '2023-05-13'),
(73, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-13'),
(74, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-13'),
(75, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-18'),
(76, 'ryacyna@gmail.com', '127.0.0.1', 'admin', '2023-05-18'),
(77, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-18'),
(78, 'ryacyna@gmail.com', '127.0.0.1', 'admin', '2023-05-18'),
(79, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-18'),
(80, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(81, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(82, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(83, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(84, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(85, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(86, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(87, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(88, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(89, 'joserijo81@gmail.com', '127.0.0.1', 'user', '2023-05-21'),
(90, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(91, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(92, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(93, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(94, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(95, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(96, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(97, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(98, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(99, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(100, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(101, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(102, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(103, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(104, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(105, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(106, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(107, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(108, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(109, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(110, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(111, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(112, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(113, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(114, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(115, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(116, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(117, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(118, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(119, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(120, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(121, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(122, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(123, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(124, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(125, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21'),
(126, 'ciprianrandy@gmail.com', '127.0.0.1', 'admin', '2023-05-21');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `usuario` varchar(100) NOT NULL,
  `Nombre_Completo` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `pass` varchar(100) NOT NULL,
  `rol` varchar(100) NOT NULL,
  `Fecha_Reg` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `usuario`, `Nombre_Completo`, `email`, `pass`, `rol`, `Fecha_Reg`) VALUES
(29, 'Randy Ciprian', 'Randy Ciprian', 'ciprianrandy@gmail.com', '12345', 'admin', '10-05-2023'),
(30, 'MariaX', 'Maria A', 'malejandrina035@gmail.com', '1212', 'user', '2023-05-10'),
(31, 'beby', 'Starling ', 'ml20271411@gmail.com', 'ml20271411@gmail.com', 'user', '2023-05-10'),
(33, 'CarlosXK', 'Joel Gonzalez', 'neonexem@gmail.com', '1234', 'user', '2023-05-10'),
(34, 'JoelX', 'Kiko pedro', 'joelrandy86@gmail.com', '123456', 'user', '2023-05-10'),
(35, 'Nicole Prensa', 'Angely Nicol Encarnacion Prensa', 'nicole@gmail.com', '202522', 'admin', '11-05-2023'),
(36, 'JoseX', 'Jose Rijo', 'joserijo81@gmail.com', '1212', 'user', '2023-05-11'),
(37, 'coopinfo', 'Rene', 'ryacyna@gmail.com', 'coopinfo23', 'admin', '2023-05-18');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alumnos`
--
ALTER TABLE `alumnos`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `Email` (`Email`),
  ADD KEY `Curso` (`Curso`),
  ADD KEY `Nombre_Completo` (`Nombre_Completo`);

--
-- Indices de la tabla `calificaciones`
--
ALTER TABLE `calificaciones`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Materia` (`Materia`),
  ADD KEY `RA1` (`RA1`),
  ADD KEY `RA2` (`RA2`),
  ADD KEY `Nombre` (`Nombre`);

--
-- Indices de la tabla `cursos`
--
ALTER TABLE `cursos`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Curso` (`Curso`);

--
-- Indices de la tabla `materias`
--
ALTER TABLE `materias`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Materia` (`Materia`);

--
-- Indices de la tabla `quejas`
--
ALTER TABLE `quejas`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `ra1`
--
ALTER TABLE `ra1`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Total` (`Total`),
  ADD KEY `Nombre` (`Nombre`);

--
-- Indices de la tabla `ra2`
--
ALTER TABLE `ra2`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Total` (`Total`),
  ADD KEY `Nombre` (`Nombre`);

--
-- Indices de la tabla `ra3`
--
ALTER TABLE `ra3`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Nombre` (`Nombre`);

--
-- Indices de la tabla `ra4`
--
ALTER TABLE `ra4`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Nombre` (`Nombre`);

--
-- Indices de la tabla `ra5`
--
ALTER TABLE `ra5`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Nombre` (`Nombre`);

--
-- Indices de la tabla `ra6`
--
ALTER TABLE `ra6`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Nombre` (`Nombre`);

--
-- Indices de la tabla `ra7`
--
ALTER TABLE `ra7`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Nombre` (`Nombre`);

--
-- Indices de la tabla `ra8`
--
ALTER TABLE `ra8`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Nombre` (`Nombre`);

--
-- Indices de la tabla `ra9`
--
ALTER TABLE `ra9`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Nombre` (`Nombre`);

--
-- Indices de la tabla `ra10`
--
ALTER TABLE `ra10`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Nombre` (`Nombre`);

--
-- Indices de la tabla `session`
--
ALTER TABLE `session`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Email` (`Email`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `Nombre Completo` (`Nombre_Completo`),
  ADD KEY `Nombre_Completo` (`Nombre_Completo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `alumnos`
--
ALTER TABLE `alumnos`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT de la tabla `calificaciones`
--
ALTER TABLE `calificaciones`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=121;

--
-- AUTO_INCREMENT de la tabla `cursos`
--
ALTER TABLE `cursos`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `materias`
--
ALTER TABLE `materias`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `quejas`
--
ALTER TABLE `quejas`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `ra1`
--
ALTER TABLE `ra1`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=107;

--
-- AUTO_INCREMENT de la tabla `ra2`
--
ALTER TABLE `ra2`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=54;

--
-- AUTO_INCREMENT de la tabla `ra3`
--
ALTER TABLE `ra3`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `ra4`
--
ALTER TABLE `ra4`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `ra5`
--
ALTER TABLE `ra5`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `ra6`
--
ALTER TABLE `ra6`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `ra7`
--
ALTER TABLE `ra7`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `ra8`
--
ALTER TABLE `ra8`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `ra9`
--
ALTER TABLE `ra9`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `ra10`
--
ALTER TABLE `ra10`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `session`
--
ALTER TABLE `session`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=127;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `alumnos`
--
ALTER TABLE `alumnos`
  ADD CONSTRAINT `alumnos_ibfk_1` FOREIGN KEY (`Email`) REFERENCES `usuarios` (`email`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `alumnos_ibfk_2` FOREIGN KEY (`Curso`) REFERENCES `cursos` (`Curso`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `alumnos_ibfk_3` FOREIGN KEY (`Nombre_Completo`) REFERENCES `usuarios` (`Nombre_Completo`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `calificaciones`
--
ALTER TABLE `calificaciones`
  ADD CONSTRAINT `calificaciones_ibfk_1` FOREIGN KEY (`Nombre`) REFERENCES `alumnos` (`Nombre_Completo`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `ra1`
--
ALTER TABLE `ra1`
  ADD CONSTRAINT `ra1_ibfk_1` FOREIGN KEY (`Nombre`) REFERENCES `alumnos` (`Nombre_Completo`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `ra2`
--
ALTER TABLE `ra2`
  ADD CONSTRAINT `ra2_ibfk_1` FOREIGN KEY (`Nombre`) REFERENCES `alumnos` (`Nombre_Completo`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `ra3`
--
ALTER TABLE `ra3`
  ADD CONSTRAINT `ra3_ibfk_1` FOREIGN KEY (`Nombre`) REFERENCES `alumnos` (`Nombre_Completo`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `ra4`
--
ALTER TABLE `ra4`
  ADD CONSTRAINT `ra4_ibfk_1` FOREIGN KEY (`Nombre`) REFERENCES `alumnos` (`Nombre_Completo`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `ra5`
--
ALTER TABLE `ra5`
  ADD CONSTRAINT `ra5_ibfk_1` FOREIGN KEY (`Nombre`) REFERENCES `alumnos` (`Nombre_Completo`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `ra6`
--
ALTER TABLE `ra6`
  ADD CONSTRAINT `ra6_ibfk_1` FOREIGN KEY (`Nombre`) REFERENCES `alumnos` (`Nombre_Completo`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `ra7`
--
ALTER TABLE `ra7`
  ADD CONSTRAINT `ra7_ibfk_1` FOREIGN KEY (`Nombre`) REFERENCES `alumnos` (`Nombre_Completo`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `ra8`
--
ALTER TABLE `ra8`
  ADD CONSTRAINT `ra8_ibfk_1` FOREIGN KEY (`Nombre`) REFERENCES `alumnos` (`Nombre_Completo`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `ra9`
--
ALTER TABLE `ra9`
  ADD CONSTRAINT `ra9_ibfk_1` FOREIGN KEY (`Nombre`) REFERENCES `alumnos` (`Nombre_Completo`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `ra10`
--
ALTER TABLE `ra10`
  ADD CONSTRAINT `ra10_ibfk_1` FOREIGN KEY (`Nombre`) REFERENCES `alumnos` (`Nombre_Completo`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `session`
--
ALTER TABLE `session`
  ADD CONSTRAINT `session_ibfk_1` FOREIGN KEY (`Email`) REFERENCES `usuarios` (`email`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
