-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 11-09-2026 a las 20:05:52
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `hoja_vida`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cursos`
--

CREATE TABLE `cursos` (
  `id` int(11) NOT NULL,
  `hoja_vida_id` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cursos`
--

INSERT INTO `cursos` (`id`, `hoja_vida_id`, `nombre`) VALUES
(2, 3, 'curso de java');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudios`
--

CREATE TABLE `estudios` (
  `id` int(11) NOT NULL,
  `hoja_vida_id` int(11) NOT NULL,
  `nivel` varchar(100) DEFAULT NULL,
  `institucion` varchar(150) DEFAULT NULL,
  `titulo` varchar(150) DEFAULT NULL,
  `anio_graduacion` year(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estudios`
--

INSERT INTO `estudios` (`id`, `hoja_vida_id`, `nivel`, `institucion`, `titulo`, `anio_graduacion`) VALUES
(1, 4, 'Tecnólogo', 'SENA', 'Análisis y Desarrollo de Software', '2026');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `experiencias`
--

CREATE TABLE `experiencias` (
  `id` int(11) NOT NULL,
  `hoja_vida_id` int(11) NOT NULL,
  `empresa` varchar(150) NOT NULL,
  `cargo` varchar(100) DEFAULT NULL,
  `tiempo` varchar(100) DEFAULT NULL,
  `funciones` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `experiencias`
--

INSERT INTO `experiencias` (`id`, `hoja_vida_id`, `empresa`, `cargo`, `tiempo`, `funciones`) VALUES
(1, 4, 'flux wear', 'programador', '2 año', 'programar paginas web'),
(2, 3, 'Restaurante El Sabor', 'Auxiliar', '1 año', 'Atender clientes, organizar productos y apoyar en las diferentes actividades');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `habilidades`
--

CREATE TABLE `habilidades` (
  `id` int(11) NOT NULL,
  `experiencia_id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `habilidades`
--

INSERT INTO `habilidades` (`id`, `experiencia_id`, `nombre`) VALUES
(2, 2, 'apoyo emocional');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `hojas_vida`
--

CREATE TABLE `hojas_vida` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `edad` int(11) DEFAULT NULL,
  `ciudad` varchar(100) DEFAULT NULL,
  `correo` varchar(150) NOT NULL,
  `fotografia` varchar(255) DEFAULT NULL,
  `programa` varchar(150) DEFAULT NULL,
  `ficha` varchar(20) DEFAULT NULL,
  `jornada` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `hojas_vida`
--

INSERT INTO `hojas_vida` (`id`, `nombre`, `edad`, `ciudad`, `correo`, `fotografia`, `programa`, `ficha`, `jornada`) VALUES
(3, 'jesus', 21, 'barramquilla', 'jesus@gmail.com', 'foto.jpg', 'ADSO', '3262320', 'diurna'),
(4, 'johan', 18, 'bogota', 'johan@gmail.com', 'foto.jpg', 'diseño', '212524', 'diurna'),
(5, 'thomas', 19, 'bogota', 'thomas@gmail.com', 'foto.jpg', 'fotografia', '2255984', 'diurna');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cursos`
--
ALTER TABLE `cursos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `hoja_vida_id` (`hoja_vida_id`);

--
-- Indices de la tabla `estudios`
--
ALTER TABLE `estudios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `hoja_vida_id` (`hoja_vida_id`);

--
-- Indices de la tabla `experiencias`
--
ALTER TABLE `experiencias`
  ADD PRIMARY KEY (`id`),
  ADD KEY `hoja_vida_id` (`hoja_vida_id`);

--
-- Indices de la tabla `habilidades`
--
ALTER TABLE `habilidades`
  ADD PRIMARY KEY (`id`),
  ADD KEY `experiencia_id` (`experiencia_id`);

--
-- Indices de la tabla `hojas_vida`
--
ALTER TABLE `hojas_vida`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `cursos`
--
ALTER TABLE `cursos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `estudios`
--
ALTER TABLE `estudios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `experiencias`
--
ALTER TABLE `experiencias`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `habilidades`
--
ALTER TABLE `habilidades`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `hojas_vida`
--
ALTER TABLE `hojas_vida`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `cursos`
--
ALTER TABLE `cursos`
  ADD CONSTRAINT `cursos_ibfk_1` FOREIGN KEY (`hoja_vida_id`) REFERENCES `hojas_vida` (`id`);

--
-- Filtros para la tabla `estudios`
--
ALTER TABLE `estudios`
  ADD CONSTRAINT `estudios_ibfk_1` FOREIGN KEY (`hoja_vida_id`) REFERENCES `hojas_vida` (`id`);

--
-- Filtros para la tabla `experiencias`
--
ALTER TABLE `experiencias`
  ADD CONSTRAINT `experiencias_ibfk_1` FOREIGN KEY (`hoja_vida_id`) REFERENCES `hojas_vida` (`id`);

--
-- Filtros para la tabla `habilidades`
--
ALTER TABLE `habilidades`
  ADD CONSTRAINT `habilidades_ibfk_1` FOREIGN KEY (`experiencia_id`) REFERENCES `experiencias` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
