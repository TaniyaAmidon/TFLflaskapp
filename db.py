import psycopg2

def connect_to_db(dbname, dbuser, dbhost, dbpass):
    return psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpass)


