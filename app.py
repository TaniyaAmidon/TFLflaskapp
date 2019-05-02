from flask import Flask, render_template
import requests
import psycopg2
import json


app = Flask(__name__)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

con = psycopg2.connect(dbname='flaskapp', user='taniyaamidon', host='localhost', password='password')

cur = con.cursor()
# cur.execute("CREATE TABLE IF NOT EXISTS results (id serial PRIMARY KEY, name varchar, email varchar)")
# con.commit()


r = requests.get('https://api.tfl.gov.uk/StopPoint/490009333W/arrivals').content
jsonResponse = json.loads(r.decode('utf-8'))


@app.route('/')
def display():
  return render_template('home.html', data=jsonResponse)


@app.route('/history')
def history():
  return render_template('history.html')


if __name__ == '__main__':
  app.run()
