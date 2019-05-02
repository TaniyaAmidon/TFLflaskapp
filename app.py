from flask import Flask, render_template

app = Flast(__name__)

@app.route('/')
  def exceptedArrivals():
    return render_template('home.html')


if __name__ == '__main__':
  app.run(debug = True)
