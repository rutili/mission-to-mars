  
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scrape 

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():
    
    mars_data = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scraper(): 
    scrape_result = mars_scrape.scrape()
    mongo.db.mars.update({},scrape_result,upsert = True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)