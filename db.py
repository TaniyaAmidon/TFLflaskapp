import psycopg2

def connect_to_db(dbname, dbuser, dbhost, dbpass):
    return psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpass)

def create_table(con):
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS history (id SERIAL PRIMARY KEY, expectedArrival timestamptz, time_timestamp timestamptz)")
    con.commit()

def store_history(con,item):
    cur = con.cursor()
    cur.execute(
        "INSERT INTO history (expectedArrival, time_timestamp ) VALUES (%s, %s)", 
        (item['expectedArrival'], item['timestamp'])
        )
    con.commit()

def fetch_history(con):
    cur = con.cursor()
    cur.execute("SELECT * FROM history")
    return cur.fetchall()