import sqlite3

conn = sqlite3.connect("python_meetup.sqlite")
cur = conn.cursor()
table_name = "meetup_data"
cur.execute("DROP TABLE IF EXISTS " + table_name)
cur.execute("""CREATE TABLE {} (
           date varchar(255),
           permit varchar(255),
           type varchar(255),
           project_name varchar(1000),
           addr varchar(255)
       );
            """.format(table_name))


cur.execute("""INSERT INTO {0}
            VALUES('{1}','{2}','{3}','{4}','{5}');""".format(
                table_name,
                "10/10/2017",
                "B123455",
                "Building",
                "Repairing a roof",
                "456 Main St. Roseville, CA 95661",
                ))
conn.commit()

cur.execute('SELECT * FROM {}'.format(table_name))
data = cur.fetchall()
print(data)
