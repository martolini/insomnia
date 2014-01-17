CREATE TABLE `insomnia` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `postid` int(11) DEFAULT NULL,
  `thedate` date DEFAULT NULL,
  `url` varchar(150) DEFAULT NULL,
  `title` varchar(200) DEFAULT NULL,
  `text` text,
  `username` varchar(80) DEFAULT NULL,
  `question` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_postid` (`postid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;