import os, sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from yoyo import step

steps = [
    step(
        """INSERT INTO `math_achievements`(`id`,`name`,`size`,`description`) VALUES(1,'light',100,'Реши 100 простых примеров');"""
    ),
    step(
        """INSERT INTO `math_achievements`(`id`,`name`,`size`,`description`) VALUES(2,'hard',100,'Реши 100 сложных примеров');"""
    ),
]
