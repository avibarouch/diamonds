from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'db_diamonds'

TABLES = {}
TABLES['diamonds'] = (
    "CREATE TABLE `diamonds` ("
    "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `carat` float(64) NOT NULL,"
    "  `cut` enum('Fair','Good','Idial','Premium','Very Good',) NOT NULL,"
    "  `color` enum('D','E','F','G','H','I','J') NOT NULL,"
    "  `clarity` enum('I1','IF','SI1','SI2','VS1','VS2','VVS1','VVS2') NOT NULL,"
    "  `depth` float(64) NOT NULL,"
    "  `table` float(64) NOT NULL,"
    "  `price` int(64) NOT NULL,"
    "  `x` varchar(64) NOT NULL,"
    "  `y` varchar(64) NOT NULL,"
    "  `z` float(64) NOT NULL,"
    "  PRIMARY KEY (`emp_no`)"
    ") ENGINE=InnoDB")
