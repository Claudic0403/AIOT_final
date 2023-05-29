import mysql.connector

# Establish a connection to the MySQL database
cnx = mysql.connector.connect(
    host="192.168.1.118",
    user="4109064206",
    password="4109064206",
    database="aiotdb"
)

# Create a cursor object
cursor = cnx.cursor()
a = 25
# Execute the query with the data
cursor.execute("INSERT INTO project_table (signal_type, PoP12h, T) VALUES ('d', {}, {})".format(10, 27))

# Commit the changes
cnx.commit()

# Close the cursor and the connection
cursor.close()
cnx.close()