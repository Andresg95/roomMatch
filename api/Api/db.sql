CREATE TABLE `tfgtest`.`rooms`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `state` VARCHAR(20) NOT NULL,
    PRIMARY KEY(`id`)
) ENGINE = INNODB; CREATE TABLE `tfgtest`.`matches`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `room_id` INT NOT NULL,
    PRIMARY KEY(`id`)
) ENGINE = INNODB; CREATE TABLE `tfgtest`.`residents`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `public_id` VARCHAR(50) NOT NULL,
    `name` VARCHAR(30) NOT NULL,
    `lastName` VARCHAR(50) NOT NULL,
    `sharedRoom` BOOLEAN NOT NULL,
    PRIMARY KEY(`id`),
    UNIQUE(`public_id`)
) ENGINE = INNODB; CREATE TABLE `tfgtest`.`testR`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `gender` VARCHAR(10) NOT NULL,
    `age` VARCHAR(10) NOT NULL,
    `musicGender` VARCHAR(25) NOT NULL,
    `sport` VARCHAR(25) NOT NULL,
    `hobbie` VARCHAR(25) NOT NULL,
    `movieSeries` VARCHAR(10) NOT NULL,
    `filmGender` VARCHAR(10) NOT NULL,
    `tabaco` VARCHAR(2) NOT NULL,
    `alcohol` VARCHAR(2) NOT NULL,
    `party` VARCHAR(2) NOT NULL,
    `ordenConvivencia` INT(2) NOT NULL,
    `ordenPersonal` INT(2) NOT NULL,
    `personalidad` VARCHAR(10) NOT NULL,
    PRIMARY KEY(`id`)
) ENGINE = INNODB; CREATE TABLE `tfgtest`.`user`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `public_id` VARCHAR(50) NOT NULL,
    `userName` VARCHAR(20) NOT NULL,
    `password` VARCHAR(80) NOT NULL,
    `admin` BOOLEAN NOT NULL,
    PRIMARY KEY(`id`),
    UNIQUE(`public_id`)
) ENGINE = INNODB; CREATE TABLE `tfgtest`.`todo`(
    `id` INT NOT NULL,
    `text` VARCHAR(50) NOT NULL,
    `complete` BOOLEAN NOT NULL,
    `user_id` INT NOT NULL,
    PRIMARY KEY(`id`)
) ENGINE = INNODB;