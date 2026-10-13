-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 12-10-2026 a las 18:10:27
-- Versión del servidor: 8.0.17
-- Versión de PHP: 7.3.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `ecotech`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asignacion_emp`
--

CREATE TABLE `asignacion_emp` (
  `asignacion_id` int(11) NOT NULL,
  `empleado_id` int(11) NOT NULL,
  `proyecto_id` int(11) NOT NULL,
  `rol` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `asignacion_emp`
--

INSERT INTO `asignacion_emp` (`asignacion_id`, `empleado_id`, `proyecto_id`, `rol`) VALUES
(2, 2, 5, 'desarrollador'),
(3, 3, 5, 're'),
(4, 3, 7, 'fd');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `departamento`
--

CREATE TABLE `departamento` (
  `user_id` int(11) NOT NULL,
  `nombre` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `gerente_empleado_id` int(11) DEFAULT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `departamento`
--

INSERT INTO `departamento` (`user_id`, `nombre`, `gerente_empleado_id`, `descripcion`) VALUES
(4, 'za', NULL, 'fdfd'),
(5, 'aa', NULL, 'aa');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado`
--

CREATE TABLE `empleado` (
  `user_id` int(11) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `salario` int(11) NOT NULL,
  `departamento_id` int(11) NOT NULL,
  `run` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `direccion` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telefono` int(11) NOT NULL,
  `correo` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `empleado`
--

INSERT INTO `empleado` (`user_id`, `fecha_inicio`, `salario`, `departamento_id`, `run`, `nombre`, `direccion`, `telefono`, `correo`) VALUES
(3, '2002-12-21', 32, 4, '2112', 'dfgasdf', 'werweqr', 123, 'asdfg'),
(4, '2002-03-12', 123, 5, '123', 'eqwe', 'sadf', 123, 'sdasdaf');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proyecto`
--

CREATE TABLE `proyecto` (
  `user_id` int(11) NOT NULL,
  `nombre` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_inicio` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `proyecto`
--

INSERT INTO `proyecto` (`user_id`, `nombre`, `descripcion`, `fecha_inicio`) VALUES
(5, 'aa', 'aa', '2002-12-20'),
(6, 'sadf', 'fadf', '2002-12-21'),
(7, 'asdf', 'asd', '2002-12-25');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_tiempo`
--

CREATE TABLE `registro_tiempo` (
  `user_id` int(11) NOT NULL,
  `empleado_id` int(11) NOT NULL,
  `proyecto_id` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `horas` int(11) NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `registro_tiempo`
--

INSERT INTO `registro_tiempo` (`user_id`, `empleado_id`, `proyecto_id`, `fecha`, `horas`, `descripcion`) VALUES
(1, 2, 5, '2002-12-24', 5, 'adsdas'),
(3, 3, 5, '2002-12-23', 3, 'sdf'),
(4, 3, 5, '2002-12-23', 23, 'sdaf');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `asignacion_emp`
--
ALTER TABLE `asignacion_emp`
  ADD PRIMARY KEY (`asignacion_id`),
  ADD KEY `fk_asignacion_empleado` (`empleado_id`),
  ADD KEY `fk_asignacion_proyecto` (`proyecto_id`);

--
-- Indices de la tabla `departamento`
--
ALTER TABLE `departamento`
  ADD PRIMARY KEY (`user_id`),
  ADD KEY `fk_departamento_gerente` (`gerente_empleado_id`);

--
-- Indices de la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD PRIMARY KEY (`user_id`),
  ADD KEY `fk_empleado_departamento` (`departamento_id`);

--
-- Indices de la tabla `proyecto`
--
ALTER TABLE `proyecto`
  ADD PRIMARY KEY (`user_id`);

--
-- Indices de la tabla `registro_tiempo`
--
ALTER TABLE `registro_tiempo`
  ADD PRIMARY KEY (`user_id`),
  ADD KEY `fk_registro_empleado` (`empleado_id`),
  ADD KEY `fk_registro_proyecto` (`proyecto_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `asignacion_emp`
--
ALTER TABLE `asignacion_emp`
  MODIFY `asignacion_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `departamento`
--
ALTER TABLE `departamento`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `empleado`
--
ALTER TABLE `empleado`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `proyecto`
--
ALTER TABLE `proyecto`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `registro_tiempo`
--
ALTER TABLE `registro_tiempo`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `asignacion_emp`
--
ALTER TABLE `asignacion_emp`
  ADD CONSTRAINT `fk_asignacion_proyecto` FOREIGN KEY (`proyecto_id`) REFERENCES `proyecto` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD CONSTRAINT `fk_empleado_departamento` FOREIGN KEY (`departamento_id`) REFERENCES `departamento` (`user_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

--
-- Filtros para la tabla `registro_tiempo`
--
ALTER TABLE `registro_tiempo`
  ADD CONSTRAINT `fk_registro_proyecto` FOREIGN KEY (`proyecto_id`) REFERENCES `proyecto` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
