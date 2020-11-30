from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#Create an instance of Flask
app = Flask(__name__)

#Connect to the mongodb database
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

@app.route('/')
def home():
    mars_data = mongo.db.collection.find_one()

    return render_template("index.html", mars = mars_data)

@app.route('/scrape')
def scrape():

    mars_scrape = scrape_mars.scrape()

    for i in range(len(mars_scrape)):
        mongo.db.collection.update({}, mars_scrape[i], upsert = True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)