import mysql.connector
from mysql.connector import errorcode
from flask import *


# On this file:
# 1.    make a connection to the database
# 2.    Create a database (if it isn't exist)
# 3.    Create a table (if it isn't exist)
# 4.    insert diamonds data (53K lines) to data base
DB_NAME = "dp_diamonds"


def drop_database(cursor):
    try:
        cursor.execute("DROP DATABASE {} ".format(DB_NAME))
    except mysql.connector.Error as err:
        return 0
    else:
        return 1


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        return 0
    else:
        return 1


def start(drop=0, **kwargs):
    # ToDo: good practic is to put this config object in a diffrent file
    #       and name it config.ini. This is because it probebly will serv
    #       other modules
    config = {
        'user': 'root',
        'password': 'root5464^%$GHFD&^*nbvn',
        'host': 'localhost',

    }
#         'raise_on_warnings': 'True',

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
            flash("Failed droping the database: {}".format(DB_NAME))
    if (cursor) and not drop:
        try:
            cursor.execute("USE {}".format(DB_NAME))
        except mysql.connector.Error as err:
            flash("Database {} does not exists.".format(DB_NAME))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                if create_database(cursor):
                    flash("Database {} created successfully."
                          .format(DB_NAME))
                else:
                    flash("Database {} not created successfully."
                          .format(DB_NAME))
                cnx.database = DB_NAME
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
                    flash("   but it's already exists.")
                else:
                    flash(err.msg)
            else:
                flash("   SUCCESS")

    cursor.close()
    cnx.close()
