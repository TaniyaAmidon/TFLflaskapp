from flask import Flask, render_template
import requests
import psycopg2

app = Flask(__name__)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

con = psycopg2.connect(dbname='flaskapp', user='taniyaamidon', host='localhost', password='password')

cur = con.cursor()
# cur.execute("CREATE TABLE IF NOT EXISTS results (id serial PRIMARY KEY, name varchar, email varchar)")
# con.commit()

@app.route('/')
def exceptedArrivals():
  return requests.get('https://api.tfl.gov.uk/StopPoint/490009333W/arrivals').content
  return render_template('home.html')
  # cur.execute("INSERT INTO results VALUES (5, 'value2', 'Value3')")
  # con.commit()
  # cur.close()
  # con.close()
  #return requests.get('https://api.tfl.gov.uk/StopPoint/490009333W/arrivals').content


@app.route('/history')
def history():
  return render_template('history.html')


if __name__ == '__main__':
  app.run()
