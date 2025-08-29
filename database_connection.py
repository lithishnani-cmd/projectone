import mysql.connector
from mysql.connector import Error

try:
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Lithishnani555@",
        database="nanidata"
    )
    cursor = conn.cursor()

    # (Optional) Explicitly select the nanidata database
    cursor.execute("USE nanidata")

    # Query the emp_data table
    cursor.execute("SELECT * FROM emp_record_table")
    rows = cursor.fetchall()

    print("Rows in emp_record_table:")
    for row in rows:
        print(row)

except Error as err:
    print("Error:", err)

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("Connection closed")
