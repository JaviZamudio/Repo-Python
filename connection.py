try:
    import mysql.connector
except:
    import os
    os.system("pip install mysql-connector-python")
    import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor

def dbConnect() -> MySQLConnection:
    return mysql.connector.connect(
        #host = "Soporte320a.huawei.net",
        host = "localhost",
        user = "root",
        password = "elihu100",
        database = "repo"
    )
def createCursor(connection: MySQLConnection) -> MySQLCursor:
    return connection.cursor()

connection = dbConnect()
myCursor = createCursor(connection)

def dbExecute(query: str, params: tuple = (), commit: bool = False):
    myCursor.execute(query, params)

    if(commit):
        connection.commit()

    return myCursor