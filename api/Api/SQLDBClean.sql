

CREATE TABLE `matches` (
  `id` int(11) NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `room_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `residents` (
  `id` int(11) NOT NULL,
  `public_id` varchar(50) NOT NULL,
  `name` varchar(30) NOT NULL,
  `lastName` varchar(50) NOT NULL,
  `sharedRoom` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE `rooms` (
  `id` int(11) NOT NULL,
  `state` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



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



CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `public_id` varchar(50) NOT NULL,
  `userName` varchar(20) NOT NULL,
  `password` varchar(80) NOT NULL,
  `admin` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `matches`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `room_id` (`room_id`);


ALTER TABLE `residents`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `public_id` (`public_id`);


ALTER TABLE `rooms`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `testr`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id_2` (`public_id`),
  ADD UNIQUE KEY `public_id` (`public_id`),
  ADD KEY `user_id` (`public_id`);


ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `public_id` (`public_id`);


ALTER TABLE `matches`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;


ALTER TABLE `residents`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;


ALTER TABLE `rooms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;


ALTER TABLE `testr`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;


ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;


ALTER TABLE `matches`
  ADD CONSTRAINT `matches_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `matches_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `residents` (`public_id`) ON DELETE CASCADE ON UPDATE CASCADE;


ALTER TABLE `residents`
  ADD CONSTRAINT `residents_ibfk_1` FOREIGN KEY (`public_id`) REFERENCES `user` (`public_id`) ON DELETE CASCADE ON UPDATE CASCADE;


ALTER TABLE `testr`
  ADD CONSTRAINT `testr_ibfk_1` FOREIGN KEY (`public_id`) REFERENCES `user` (`public_id`) ON DELETE CASCADE ON UPDATE CASCADE;
