import os, sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from yoyo import step

steps = [
    step(
        """CREATE TABLE `math_user` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `name` varchar(255) DEFAULT NULL,
          `password` varchar(255) DEFAULT NULL,
          `token` varchar(255) DEFAULT NULL,
          `email` varchar(255) DEFAULT NULL,
          PRIMARY KEY (`id`)
      ) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"""
    ),
    step(
        """CREATE TABLE `math_tasks` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `task` varchar(255) NOT NULL,
          `solution` float NOT NULL,
          `hard` tinyint(4) NOT NULL,
          PRIMARY KEY (`id`)
      ) ENGINE=InnoDB AUTO_INCREMENT=2601 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"""
    ),
    step(
        """CREATE TABLE `math_stat` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `0_total` int(11) DEFAULT 0,
          `0_right` int(11) DEFAULT 0,
          `0_wrong` int(11) DEFAULT 0,
          `1_total` int(11) DEFAULT 0,
          `1_right` int(11) DEFAULT 0,
          `1_wrong` int(11) DEFAULT 0,
          `2_total` int(11) DEFAULT 0,
          `2_right` int(11) DEFAULT 0,
          `2_wrong` int(11) DEFAULT 0,
          `custom_total` int(11) DEFAULT 0,
          `custom_right` int(11) DEFAULT 0,
          `custom_wrong` int(11) DEFAULT 0,
          PRIMARY KEY (`id`),
          CONSTRAINT `math_stat_ibfk_1` FOREIGN KEY (`id`) REFERENCES `math_user` (`id`)
      ) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"""
    ),
    step(
        """CREATE TABLE `math_achievements` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `name` varchar(255) DEFAULT NULL,
          `size` int(11) DEFAULT NULL,
          `description` text DEFAULT NULL,
          PRIMARY KEY (`id`)
      ) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"""
    ),
    step(
        """CREATE TABLE `math_achievements_stat` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `light` int(11) DEFAULT 0,
          `hard` int(11) DEFAULT 0,
          PRIMARY KEY (`id`),
          CONSTRAINT `math_achievements_stat_ibfk_1` FOREIGN KEY (`id`) REFERENCES `math_user` (`id`)
      ) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"""
    )
]