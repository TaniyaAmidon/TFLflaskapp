from flask import Flask, render_template
import requests
import json
import db
from dateutil import parser
from pytz import timezone
from datetime import datetime
from flask import jsonify

app = Flask(__name__)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

con = db.connect_to_db()
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS history (id SERIAL PRIMARY KEY, expectedArrival timestamptz, time_timestamp timestamptz)")
con.commit()
# cur.close()
# con.close()


@app.route('/')
def display():
  r = requests.get('https://api.tfl.gov.uk/StopPoint/490009333W/arrivals').content
  jsonResponse = json.loads(r.decode('utf-8'))

  data = []
  for item in jsonResponse:
    london_tz = timezone('Europe/London')
    dt = parser.parse(jsonResponse[0]['timestamp'])
    tt = london_tz.normalize(dt.astimezone(london_tz))
    timenow = tt.strftime('%H:%M:%S')
    dt2 = parser.parse(item['expectedArrival'])
    tt2 = london_tz.normalize(dt2.astimezone(london_tz))
    mins = dt2 - dt
    data.append(
      {
        "route": item['lineName'],
        "stop": item['stationName'],
        "destination": item['destinationName'],
        "expectedArrival": round(mins.seconds/60),
        "towards": item['towards']
      }
      )
    # data[::-1]

    cur.execute("INSERT INTO history (expectedArrival, time_timestamp ) VALUES (TIMESTAMP '" + item['expectedArrival'] + "', TIMESTAMP '" + item['timestamp'] + "')")
    con.commit()
    # cur.close()
    # con.close()
  return render_template('home.html', data=data, tx=timenow)




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
      "time_timestamp": (row[2]).strftime('%d:%m:%Y') + " / " +  (row[2]).strftime('%H:%M:%S')
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
