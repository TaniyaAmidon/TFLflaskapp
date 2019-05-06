from flask import Flask, render_template, g
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


@app.route('/')
def display():
  r = requests.get('https://api.tfl.gov.uk/StopPoint/490009333W/arrivals')
  if r.status_code != 200:
    return page_not_found("An error occured. Please try again later!")

  jsonResponse = json.loads(r.content.decode('utf-8'))

  list = []
  for item in jsonResponse:

    #timestamp conversion
    local_time_timestamp = convert_to_localtime(item['timestamp'])
    timestamp_formatted = local_time_timestamp.strftime('%H:%M:%S')

    # expected arrival
    local_time_arrivals = convert_to_localtime(item['expectedArrival'])
    arrivals_formatted = local_time_arrivals.strftime('%H:%M:%S')

    mins = local_time_arrivals - local_time_timestamp

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
    db.store_history(get_db_con(),item)

  return render_template('home.html', data=reversed_list, tx=timestamp_formatted)


@app.route('/history')
def history():
  items = db.fetch_history(get_db_con())
  info = []

  for row in items:
    local_time_timestamp = datetime_to_localtime(row[1])
    timestamp_formatted = row[1].strftime('%H:%M:%S')
    local_time_arrivals = datetime_to_localtime(row[2])
    arrivals_formatted = local_time_arrivals.strftime('%H:%M:%S')
    
    info.append(
    {
      "Id": row[0],
      "expectedArrival": timestamp_formatted,
      "time_timestamp": arrivals_formatted 
    }
    )

  return render_template('history.html', d=info)

def datetime_to_localtime(datetime):
  london_tz = timezone('Europe/London')
  return london_tz.normalize(datetime.astimezone(london_tz))

def convert_to_localtime(item):
  datetime = parser.parse(item)
  return datetime_to_localtime(datetime)
  
@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html')

@app.errorhandler(500)
def page_not_found(e):
  return render_template('500.html', error= e), 500

def get_db_con():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'db_con'):
        g.db_con = db.connect_to_db(
          app.config.get('DB_NAME'), 
          app.config.get('DB_USER'), 
          app.config.get('DB_HOST'), 
          app.config.get('DB_PASS'),
        )

    return g.db_con

@app.teardown_appcontext
def close_db_con(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db_con'):
        g.db_con.close()

def setup_db():
  with app.app_context():
    db.create_table(get_db_con())        

# Setup db tables
setup_db()

if __name__ == '__main__':
  app.run()

