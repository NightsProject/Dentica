from mysql_initializer import connectDB, createAllTables
from config.config import databaseName



#try db connection if connected then initialize all tables
conn = connectDB()
if conn:
    print(f"Successfully connected to {databaseName} database")
    createAllTables(conn)
    conn.close()
else:
    print(f"Connected Failed")

#ToDO
#Notify to gui



