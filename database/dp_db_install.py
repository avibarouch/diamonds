import mysql.connector
from mysql.connector import errorcode
import csv
# On this file:
# 1.    make a connection to the database
# 2.    Create a database (if it isn't exist)
# 3.    Create a table (if it isn't exist)
# 4.    insert diamonds data (53K lines) to data base
DB_NAME = "dp_diamonds"


def drop():
    for arg in kwargs:
        return arg[drop]


def drop_database(cursor):
    try:
        cursor.execute("DROP DATABASE {} ".format(DB_NAME))
        print("Success droping the database")
    except mysql.connector.Error as err:
        print("Failed droping the database: {}".format(err))
        exit(1)


def create_database(cursor):
    try:
        # cursor.execute("DROP DATABASE {} ".format(DB_NAME))
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


def start(**kwarg):
    # ToDo: good practic is to put this config object in a diffrent file
    #       and name it config.ini. This is because it probebly will serv 
    #       other modules
    config = {
        'user': 'root',
        'password': 'root5464^%$GHFD&^*nbvn',
        'host': 'localhost',
        'raise_on_warnings': 'True',
    }

    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = cnx.cursor()
        print("Connection for db_user is established with no errors!")

    if (cursor) & (drop()):
        create_database(cursor)
    if (cursor) and not drop():
        print("Begin instalation proccess:")
        try:
            cursor.execute("USE {}".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(DB_NAME))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                create_database(cursor)
                print("Database {} created successfully.".format(DB_NAME))
                cnx.database = DB_NAME
            else:
                print(err)
                exit(1)
        finally:
            print("Database is exist!")

        TABLES = {}
        TABLES['diamonds'] = (
            "CREATE TABLE `diamonds` ("
            "  `insert_date` DATE DEFAULT GETDATE(),"
            "  `num` INT(10),"
            "  `carat` DECIMAL(8,2),"
            "  `cut` VARCHAR(32),"
            "  `color` enum('D','E','F','G','H','I','J'),"
            "  `clarity` enum('I1','IF','SI1','SI2','VS1'"
            "  'VS2','VVS1','VVS2'),"
            "  `depth` float(6,2),"
            "  `table1` float(6,2),"
            "  `price` int(7),"
            "  `x` float(6,2),"
            "  `y` float(6,2),"
            "  `z` float(6,2),"
            "  PRIMARY KEY (`date`, `num`)"
            ") ENGINE=InnoDB")

        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Try to creat table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("but it's already exists.")
                else:
                    print(err.msg)
            else:
                print("SUCCESS")

    cursor.close()
    cnx.close()
