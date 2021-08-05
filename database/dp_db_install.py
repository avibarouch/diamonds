import mysql.connector
from mysql.connector import errorcode
import csv
# On this installation:
# 1.    Create a database (if it isn't exist)
# 2.    Create a table (if it isn't exist)

DB_NAME = "dp_diamonds"


def create_database(cursor):
    try:
        # cursor.execute("DROP DATABASE {} ".format(DB_NAME))
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


def start():
    config = {
      'user': 'root',
      'password': 'root5464^%$GHFD&^*nbvn',
      'host': 'localhost',
      'raise_on_warnings': True
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
        "  `date` DATE,"
        "  `num` INT(10),"
        "  `carat` DECIMAL(8,2),"
        "  `cut` enum('Fair','Good','Idial','Premium','Very Good'),"
        "  `color` enum('D','E','F','G','H','I','J'),"
        "  `clarity` enum('I1','IF','SI1','SI2','VS1','VS2','VVS1','VVS2'),"
        "  `depth` float(6,2),"
        "  `table` float(6,2),"
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

# CONVERT (DATE, GETDATE())
#    sql_query = """
#    INSERT INTO `diamonds` (`date`, `carat`, `cut`, `color`, `clarity`, `depth`, `table`, `x`, `y`, `z`)
#    VALUES
#        '2021-01-01',,,,,,,,,,,,
#    )
#    """
#    print(sql_query)
#    cursor.execute(sql_query)

    f = open('data/diamonds.csv', newline='')
    f1 = csv.reader(f, delimiter=',')
#    for row in f1:
#        print(',  '.join(row))
#    csvfile = open('data/diamonds.csv')
#    head_line = csvfile.readline().strip("\n")
#    key = head_line.split(",")
#    csvfile.__next__()
#    for line in csvfile:
#        line = line.strip('\n')
#        val = line.split(",")
#        dic[key] = val

    cursor.close()
    cnx.close()
