from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'db_diamonds'

TABLES = {}
TABLES['diamonds'] = (
    "CREATE TABLE `diamonds` ("
    "  `diamind_no` INT(6) UNSIGEND AUTO_INCREMENT,"
    "  `carat` DECIMAL(8,2) ,"
    "  `cut` enum('Fair','Good','Idial','Premium','Very Good',),"
    "  `color` enum('D','E','F','G','H','I','J') NOT NULL,"
    "  `clarity` enum('I1','IF','SI1','SI2','VS1','VS2','VVS1','VVS2'),"
    "  `depth` float(6,2),"
    "  `table` float(6,2),"
    "  `price` int(7,0),"
    "  `x` varchar(6,2),"
    "  `y` varchar(6,2) ,"
    "  `z` float(6,2),"
    "  PRIMARY KEY (`diamond_no`)"
    ") ENGINE=InnoDB")
