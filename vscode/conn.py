import mysql.connector

cnx = mysql.connector.connect(user='root', password='P@ssw0rd',
                              host='127.0.0.1', port=3307, 
                              database='ai2025c')
cnx.close()