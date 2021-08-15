# from __future__ import print_function
# from datetime import date, datetime, timedelta
from flask import *
from mysql.connector import errorcode
import mysql.connector
# import dp_db_connection
db_name = "diamonds"


def me(diamond):
    # This function add new diamond goten from the user of a form in
    # the file: template/addnew.html.
    # The function arange the diamond data to a SQL statment to insert
    # into the database.
    # it returns true uf the diamond was inserted to database.
    #
    # ToDo: As we mention befor it is good practic to make from this config
    # object a bigger object together with the logic from down here to a
    # different python file This is because it probebly will serv other
    # modules
    config = {
        'user': 'root',
        'password': 'root5464^%$GHFD&^*nbvn',
        'host': 'localhost',
        'autocommit': 'True'}

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

    if (cursor):
        try:
            cursor.execute("USE {}".format(db_name))
        except mysql.connector.Error as err:
            flash("Database {} does not exists or need repeair."
                  .format(db_name))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                flash("Database does not exist")
            flash(err)
    else:
        cursor = cnx.cursor()
        flash("Connection to MySQL server established with no errors!")
    v = diamond
    for key in v:
        try:
            float(v[key])
        except (ValueError):
            pass  # Don't change the strings like "vGood" cut
        else:
            v[key] = round(float(v[key]), 2)  # convert the string goten
            if v[key] <= 0:
                v[key] = 'NULL'  # Negativ numbers become empty value
            if key == 6:  # This is the price
                v[key] = int(v[key])
    sql = "INSERT INTO `diamonds` (`carat`,`cut`,`color`"
    sql += ",`clarity`,`depth`,`table1`,`price`,`x`,`y`,`z`) "
    sql += ("VALUES ({}, ").format(v[0])
    sql += ('"'+'{}'+'",').format(v[1])
    sql += ('"'+'{}'+'",').format(v[2])
    sql += ('"'+'{}'+'",').format(v[3])
    sql += "{},{},{},{},{},{})".format(v[4], v[5], v[6], v[7], v[8], v[9])
    try:
        cursor.execute(sql)
        flash("Diamond inserted to database sucssesfuly")
        cnx.commit()
        inserted = True
    except mysql.connector.Error as err:
        flash("Something went wrong: {}".format(err))
        inserted = False
    finally:
        cursor.close()
        cnx.close()
        if (inserted):
            return 1
        else:
            return 0
