import mysql.connector
from mysql.connector import errorcode
from flask import *
import csv
import sys
import dp_functions
csv_file = "diamonds.csv"
db_name = "diamonds"


def request_clean_data(diamond):
    diamond[num] = strip(request(num), "'")


def file_exist_test(file):
    # This is a test of te existence of a file
    # Get a name and relativ path to the file
    # Return 1 if the file was found
    try:
        flash("Try to find a csv file")
        open(csv_file)
    except OSError as err:
        flash("OS error, Pleas check if the file exist")
        return 0
    else:
        flash("The file was founded")
        return 1


def insert_data(cursor):
    # The wanted result on the first faze is a string like below
    #   on the next faze we try to insert it to the table
    #   INSERT INTO `diamonds` (`num`,`carat`,`cut`,`color`,
    #   `clarity`,`depth`,`table1`,`price`,`x`,`y`,`z`) VALUES (2,
    #   0.21,"Premium","E","SI1", 59.8,61,326,3.89,3.84,2.31)
    inserted_sucssesfuly = 0
    i = 0
    with open(csv_file, newline='') as file:
        diamond_reader = csv.reader(file)
        for line in diamond_reader:
            if i >= 1:
                v = line  # For values
                sql = "INSERT INTO `diamonds` (`num`,`carat`,`cut`,`color`"
                sql += ",`clarity`,`depth`,`table1`,`price`,`x`,`y`,`z`) "
                sql += ("VALUES ({},{},").format(v[0], v[1])
                sql += ('"'+'{}'+'",').format(v[2])
                sql += ('"'+'{}'+'",').format(v[3])
                sql += ('"'+'{}'+'",').format(v[4])
                sql += "{},{},{},{},{},{})".format(v[5], v[6], v[7], v[8],
                                                   v[9], v[10])
                try:
                    cursor.execute(sql)
                    inserted_sucssesfuly += 1
                except:
                    flash(v[0])
            i += 1
    return inserted_sucssesfuly


def drop_database(cursor):
    try:
        cursor.execute("DROP DATABASE {} ".format(db_name))
    except mysql.connector.Error as err:
        return 0
    else:
        return 1


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
    except mysql.connector.Error as err:
        return 0
    else:
        return 1


def start(drop=0, addnew=0, **kwargs):
    # ToDo: good practic is to put this config object in a diffrent file
    #       and name it config.ini. This is because it probebly will serv
    #       other modules
    config = {
        'user': 'root',
        'password': 'root5464^%$GHFD&^*nbvn',
        'host': 'localhost',
        'autocommit': 'True',
    }

    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            flash("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            flash("Database does not exist")
        else:
            flash(err)
    else:
        cursor = cnx.cursor()
        flash("Connection for db_user is established with no errors!")

    if (cursor) and (drop):
        if drop_database(cursor):
            flash("Database droped")
        else:
            flash("Database is not Exist: {}".format(db_name))
    if (cursor) and not drop:
        try:
            cursor.execute("USE {}".format(db_name))
        except mysql.connector.Error as err:
            flash("Database {} does not exists.".format(db_name))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                if create_database(cursor):
                    flash("Database {} created successfully."
                          .format(db_name))
                else:
                    flash("Database {} not created successfully."
                          .format(db_name))
                cnx.database = db_name
            else:
                flash(err)
        else:
            flash("Database Exist and redy")

        TABLES = {}
        TABLES['diamonds'] = (
            "CREATE TABLE `diamonds` ("
            "  `time_stamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
            "  `num` INT(10),"
            "  `carat` DECIMAL(8,2),"
            "  `cut` VARCHAR(32),"
            "  `color` enum('D','E','F','G','H','I','J'),"
            "  `clarity` enum('I1','IF','SI1','SI2','VS1',"
            "  'VS2','VVS1','VVS2'),"
            "  `depth` float(6,2),"
            "  `table1` float(6,2),"
            "  `price` int(7),"
            "  `x` float(6,2),"
            "  `y` float(6,2),"
            "  `z` float(6,2),"
            "  PRIMARY KEY (`time_stamp`, `num`)"
            ") ENGINE=InnoDB")

        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                flash("Try to creat table {}: ".format(table_name))
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    flash("Table already exists.")
                else:
                    flash(err.msg)
            else:
                flash("Table was created")
    if cursor and not drop and file_exist_test(csv_file):
        inserted_sucssesfuly = insert_data(cursor)
        flash("Number of inserted sucssesfuly diamonds is: {} "
              .format(inserted_sucssesfuly))
    if cursor and addnew:
        diamond = {}
        request_clean_data(diamond)
        create_csv_file()
        insert_new_diamond(cursor)

    cursor.close()
    cnx.close()
