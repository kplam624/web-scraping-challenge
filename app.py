# Import Dependancies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


#Create an instance of Flask
app = Flask(__name__)

#Connect to the mongodb database
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

# Create the home route
@app.route('/')
def home():
    mars_data = mongo.db.collection.find_one()

    return render_template("index.html", mars = mars_data)

# Create the scrape route
@app.route('/scrape')
def scrape():

# Start scraping
    mars_scrape = scrape_mars.scrape()

# Updates the mongo database with a new collection and updates it.
    mongo.db.collection.update({}, mars_scrape, upsert = True)

# Redirects the user to the home page.
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)