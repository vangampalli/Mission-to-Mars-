from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars_app")

@app.route("/")
def home():
   mars_mongo = mongo.db.mars_mongo.find_one()
   return render_template("index.html", mars=mars_mongo)

@app.route("/scrape")
def scraper():
    mars_mongo = mongo.db.mars_mongo
    mars_data = scrape_mars.scrape()
    mars_mongo.replace_one({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)