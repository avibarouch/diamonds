# from __future__ import print_function
# from datetime import date, datetime, timedelta
from mysql.connector import errorcode
import mysql.connector
import dp_db_connection
import csv


def dp_diamond():
    try:
        cnx = mysql.connector.connect(**dp_db_connection.DB_CONNECTION)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            create_database()
        else:
            print(err)
    else:
        cursor = cnx.cursor()
        print("Connection for db_user is established with no errors!")
        flash("Connection for db_user is established with no errors!")

    cursor.close()
    cnx.close()

    # # this form of sending values (%s) is problematic
    # add_diamond = ("INSERT INTO `dp_diamonds` "
    #               "(`carat`, `cut`, `color`, `clarity`,"
    #               " `depth`, `table`, `x`, `y`, `z`) "
    #               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    #
    # Insert diamond information
    # data_diamond = {
    #  'carat': 2.32,
    #  'cat': "Good",
    #  'color': "D",
    #  'clarity': "IF",
    #  'depth': 5.43,
    #  'table1': 3.57,
    #  'x': 3.54,
    #  'y': 4.54,
    #  'z': 7.87,
    # }
    # # insert new diamond
    # cursor.execute(add_somthing, data_diamond)

# This try was *succssesfull*
#    add_diamond = ("INSERT INTO `diamonds` "
#                   "(`carat`, `cut`, `color`, `clarity`,"
#                   " `depth`, `table1 `, `x`, `y`, `z`) "
#                   "VALUES (4.2, 'Good', 'D', 'IF', 4.2,"
#                   " 3.87, 2.4, 4.54, 7.87)")
#
#    # insert new diamond with *success*
#    try:
#        cursor.execute(add_diamond)
#    except mysql.connector.Error as err:
#        if ((err.errno == errorcode.ER_TABLE_EXISTS_ERROR)
#                or (err.errno == 1050)):
#            print("Pleas Install the dalabase first")
#        else:
#            print(err.msg)
#    else:
#        # Make sure data is committed to the database
#        cnx.commit()
#
#        print("Insert data with SUCCESS")
