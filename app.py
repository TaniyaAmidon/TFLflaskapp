from flask import Flask, render_template
import requests
import json
import db
from dateutil import parser
from pytz import timezone
from datetime import datetime
from flask import jsonify
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

con = db.connect_to_db(
  app.config.get('DB_NAME'), 
  app.config.get('DB_USER'), 
  app.config.get('DB_HOST'), 
  app.config.get('DB_PASS'),
)

db.create_db(con)

@app.route('/')
def display():
  r = requests.get('https://api.tfl.gov.uk/StopPoint/490009333W/arrivals').content
  jsonResponse = json.loads(r.decode('utf-8'))

  list = []
  for item in jsonResponse:
    london_tz = timezone('Europe/London')
    dt = parser.parse(jsonResponse[0]['timestamp'])
    tt = london_tz.normalize(dt.astimezone(london_tz))
    timenow = tt.strftime('%H:%M:%S')
    dt2 = parser.parse(item['expectedArrival'])
    tt2 = london_tz.normalize(dt2.astimezone(london_tz))
    mins = dt2 - dt
    list.append(
      {
        "route": item['lineName'],
        "stop": item['stationName'],
        "destination": item['destinationName'],
        "expectedArrival": round(mins.seconds/60),
        "towards": item['towards']
      }
      )
    # sort the expectedArrivals in descending order
    reversed_list = sorted(list, key=lambda l: l['expectedArrival'])
    store_history(con) 
  return render_template('home.html', data=reversed_list, tx=timenow)




@app.route('/history')
def history():
  cur.execute("SELECT * FROM history")
  items = cur.fetchall()
  info = []
  for row in items:
    info.append(
    {
      "Id": row[0],
      "expectedArrival": (row[1]).strftime('%H:%M:%S'),
      "time_timestamp": (row[2]).strftime('%d/%m/%Y %H:%M:%S') 
    }
    )
  return render_template('history.html', d=info)


@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html')

@app.errorhandler(500)
def page_not_found(e):
  return render_template('500.html', error= e), 500

if __name__ == '__main__':
  app.run()
