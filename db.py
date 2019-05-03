import psycopg2

def connect_to_db():
    return psycopg2.connect(dbname='tfl', user='taniyaamidon', host='localhost', password='password')


