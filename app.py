# import libraries
from flask import Flask, render_template, redirect, jsonify
import pymongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# setup mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.mars_db
collection = db.mars_facts


# route that renders index.html template and finds Mars info from MongoDB
@app.route('/')
def index():
    # Find data
    mars_info = list(collection.find({}))
    # return template and data
    return render_template("index.html", mars_info=mars_info)

# Route that trigger scrape functions
@app.route("/scrape")
def scraper():
    # Run scraped functions
    mars_data = scrape_mars.scrape()
    collection.update({}, mars_data, upsert = True)
    print("Mars weather - ", mars_data['mars_weather'])

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)