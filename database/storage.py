import configparser
import MySQLdb.cursors
# import mysql.connector
# This is a separate, easy to use, connection to My SQL handling functions
# ToDo: This file is not usable yet. Make it usable on the next version
config = configparser.ConfigParser()
config
config.read('C://Users//richter-barouch//diamonds//database//config.ini')


def connect():
    return MySQLdb.connect(
        host=config['mysqlDB']['host'],
        port=config['mysqlDB']['port'],
        user=config['mysqlDB']['user'],
        db=config['mysqlDB']['db'],
        password=config['mysqlDB'][r'password']
    )


def db_name():
    db = config['mysqlDB']['db']
    return db
