import psycopg2

conn = psycopg2.connect(database="product", user="postgres",password="",host="127.0.0.1",port="5432")
print("open")
cur = conn.cursor()
cur.execute("select * from product")
rows = cur.fetchall()
for row in rows:
   print("ID = ", row[0])
   print("NAME = ", row[1])
   print("ADDRESS = ", row[2])
   print("SALARY = ", row[3], "\n")

print("succ")
conn.close()
