import psycopg2

def connect_to_db(dbname, dbuser, dbhost, dbpass):
    return psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpass)

def create_db(con):
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS history (id SERIAL PRIMARY KEY, expectedArrival timestamptz, time_timestamp timestamptz)")
    con.commit()
# cur.close()
# con.close()

def store_history(con):
    cur = con.cursor()
    cur.execute("INSERT INTO history (expectedArrival, time_timestamp ) VALUES (TIMESTAMP '" + item['expectedArrival'] + "', TIMESTAMP '" + item['timestamp'] + "')")
    con.commit()
    # cur.close()
    # con.close()