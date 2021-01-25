-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 25-01-2021 a las 15:52:45
-- Versión del servidor: 10.4.17-MariaDB
-- Versión de PHP: 7.4.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `tfgtest`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `matches`
--

CREATE TABLE `matches` (
  `id` int(11) NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `room_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `residents`
--

CREATE TABLE `residents` (
  `id` int(11) NOT NULL,
  `public_id` varchar(50) NOT NULL,
  `name` varchar(30) NOT NULL,
  `lastName` varchar(50) NOT NULL,
  `sharedRoom` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `residents`
--

INSERT INTO `residents` (`id`, `public_id`, `name`, `lastName`, `sharedRoom`) VALUES
(1, '01e87f5e-73aa-4eca-aa91-d2207dbc5b40', 'Douglas A', 'Rodriguez Bautista', 0),
(2, '45401418-3277-48e0-9896-6d021ff615bc', 'Diego F.', 'Hernandez Reyes', 0),
(3, '6f5e581a-bb27-41bd-a13c-06d940241caa', 'Clara', 'Romes Alma', 0),
(4, 'f0f2483a-757f-4740-9ff8-72ee713b8a94', 'Jose Ramon', ' Aquino Geraldo', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rooms`
--

CREATE TABLE `rooms` (
  `id` int(11) NOT NULL,
  `state` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `testr`
--

CREATE TABLE `testr` (
  `id` int(11) NOT NULL,
  `public_id` varchar(50) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `age` varchar(10) NOT NULL,
  `musicGender` varchar(25) NOT NULL,
  `sport` varchar(25) NOT NULL,
  `hobbie` varchar(25) NOT NULL,
  `movieSeries` varchar(10) NOT NULL,
  `filmGender` varchar(10) NOT NULL,
  `tabaco` varchar(2) NOT NULL,
  `alcohol` varchar(2) NOT NULL,
  `party` varchar(2) NOT NULL,
  `ordenConvivencia` int(2) NOT NULL,
  `ordenPersonal` int(2) NOT NULL,
  `personalidad` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `testr`
--

INSERT INTO `testr` (`id`, `public_id`, `gender`, `age`, `musicGender`, `sport`, `hobbie`, `movieSeries`, `filmGender`, `tabaco`, `alcohol`, `party`, `ordenConvivencia`, `ordenPersonal`, `personalidad`) VALUES
(2, '01e87f5e-73aa-4eca-aa91-d2207dbc5b40', 'masculino', '22', 'EDM', 'Voley', 'Video Juegos', 'pelicula', 'Thriller', 'no', 'si', 'si', 8, 5, 'intro');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `public_id` varchar(50) NOT NULL,
  `userName` varchar(20) NOT NULL,
  `password` varchar(80) NOT NULL,
  `admin` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `user`
--

INSERT INTO `user` (`id`, `public_id`, `userName`, `password`, `admin`) VALUES
(1, '05b1923e-4193-49fe-8e43-0ae7f2df7717', 'admin', 'sha256$WnOkHc1f$ba99d436551b9778b381c4d87da25d3819f6a2ef8eda0e68634656fc6285370a', 1),
(2, '01e87f5e-73aa-4eca-aa91-d2207dbc5b40', 'douglas.rodriguez', 'sha256$hgOXkaet$08faca1592ccf771e02379439c56ba35fae5d35852bda4a608878c4b1c21a0b7', 1),
(3, '45401418-3277-48e0-9896-6d021ff615bc', 'diego.hernandez', 'sha256$PaeWf2Lt$c9bddc4df72cdf91d152894b952891fb2881ec168a77ff9128da59676a68d53b', 0),
(4, '6f5e581a-bb27-41bd-a13c-06d940241caa', 'clara.romes', 'sha256$ozWcmYzr$52cb5c6f2e6c351e501084037c3a7cda6500aa92dd96c1e80f2d2f9514355c49', 0),
(5, 'f0f2483a-757f-4740-9ff8-72ee713b8a94', 'jose.ramon', 'sha256$oa7sEXo6$b8086f98197d7a49cd1a0628aa3953f8a8c74a29e8f8a4ca717782a54ee0f4ba', 0);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `matches`
--
ALTER TABLE `matches`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `room_id` (`room_id`);

--
-- Indices de la tabla `residents`
--
ALTER TABLE `residents`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `public_id` (`public_id`);

--
-- Indices de la tabla `rooms`
--
ALTER TABLE `rooms`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `testr`
--
ALTER TABLE `testr`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id_2` (`public_id`),
  ADD UNIQUE KEY `public_id` (`public_id`),
  ADD KEY `user_id` (`public_id`);

--
-- Indices de la tabla `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `public_id` (`public_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `matches`
--
ALTER TABLE `matches`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `residents`
--
ALTER TABLE `residents`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `rooms`
--
ALTER TABLE `rooms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `testr`
--
ALTER TABLE `testr`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `matches`
--
ALTER TABLE `matches`
  ADD CONSTRAINT `matches_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `matches_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `residents` (`public_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `residents`
--
ALTER TABLE `residents`
  ADD CONSTRAINT `residents_ibfk_1` FOREIGN KEY (`public_id`) REFERENCES `user` (`public_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `testr`
--
ALTER TABLE `testr`
  ADD CONSTRAINT `testr_ibfk_1` FOREIGN KEY (`public_id`) REFERENCES `user` (`public_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
