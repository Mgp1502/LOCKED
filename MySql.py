import mysql.connector
import DB_Settings


def insert_key(data_tuple):
    try:
        connection = mysql.connector.connect(host=DB_Settings.DB_HOST,
                                             database=DB_Settings.DB_DATABASE,
                                             user=DB_Settings.DB_USER,
                                             password=DB_Settings.DB_PASS)

        if connection.is_connected():
            cursor = connection.cursor()

            mySql_insert_query = """REPLACE INTO entry (name, dungeon, level) 
                                    VALUES (%s, %s, %s)"""

            cursor.execute(mySql_insert_query, data_tuple)
            connection.commit()
            print("Succesfully inserted/updated a entry")

    except mysql.connector.Error as e:
        print("Error while querying to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Closed DB connection")
