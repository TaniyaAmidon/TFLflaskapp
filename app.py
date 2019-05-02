from flask import Flask, render_template

app = Flask(__name__)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

@app.route('/')
def exceptedArrivals():
  return render_template('home.html')

@app.route('/history')
def history():
  return render_template('history.html')


if __name__ == '__main__':
  app.run()
