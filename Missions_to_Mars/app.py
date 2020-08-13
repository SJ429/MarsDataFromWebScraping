from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scrape 


app = Flask(__name__)

# setup mongo connection and connect to mongo db 

app.config["MONGO_URI"] ="mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

  # Establish home route

@app.route("/")
def home():

    # Render an index.html template and pass in the data retrieved from the database

    mars_data= mongo.db.mars_data

        
    return render_template("index.html", mars_data=mars_data)

    # Scrape function   
@app.route("/scrape")
def scrape():

    # drop any data that is already in database
    #mongo.db.mars_data.drop()

    # Run scrape function
    mars_data = mongo.db.mars_data
    
    mars_data = mars_scrape.scrape()

    # Update mars db in mongo
    mongo.db.mars_data.update({}, mars_data, upsert=True)

    # Return to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    
    app.run(debug=True)
