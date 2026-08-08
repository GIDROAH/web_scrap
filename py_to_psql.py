import psycopg2

try:
    conn = psycopg2.connect(
        dbname = 'studentdb',
        user = 'postgres',
        password = 'gidorah',
        host = 'localhost',
        port = '5432'
    )

    print("Database connection successful!")

except Exception as e:
    print(f'Database connection failed: {e}')

cur = conn.cursor()

cur.execute('select name, age from students where age > 20;')
            
rows = cur.fetchall()
for row in rows:
    print(row)


cur.execute("INSERT INTO Students (name, age) VALUES (%s, %s)", ("Rahul", 22))
conn.commit()


cur.close()
conn.close()
