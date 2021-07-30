import mysql.connector

config = {
  'user': 'avibarouch@gmail.com',
  'password': 'nhsg2021',
  'host': '127.0.0.1',
  'database': 'db_diamonds',
  'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)

cnx.close()
