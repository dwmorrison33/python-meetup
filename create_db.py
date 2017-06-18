import sqlite3

conn = sqlite3.connect("python_meetup.sqlite")
cur = conn.cursor()
table_name = "permit_data"
cur.execute("DROP TABLE IF EXISTS " + table_name)
cur.execute("""CREATE TABLE {} (
           date_issued varchar(255),
           permit_number varchar(255),
           permit_type varchar(255),
           description varchar(1000),
           address varchar(255),
           status varchar(525)
       );
            """.format(table_name))


cur.execute("""INSERT INTO {0}
            VALUES('{1}','{2}','{3}','{4}','{5}','{6}');""".format(
                table_name,
                "10/10/2017",
                "B123455",
                "Building",
                "Repairing a roof",
                "456 Main St. Roseville, CA 95661",
                "Issued",
                ))
conn.commit()

cur.execute('SELECT * FROM {}'.format(table_name))
data = cur.fetchall()
print(data)
