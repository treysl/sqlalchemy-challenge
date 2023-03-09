import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
import os
file_path = os.path.join("Resources/hawaii.sqlite")
engine = create_engine(file_path)
base = automap_base()
base.prepare(autoload_with=engine)

measurement = base.classes.measurement
station = base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = sqlalchemy(app)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

#################################################
# Design the Climate App
#################################################
    
###Convert the query results from your precipitation analysis 
###(i.e. retrieve only the last 12 months of data) to a dictionary 
###using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= '2016-08-23').\
    filter(measurement.date <= '2017-08-23').\
    order_by(measurement.date).all()
    session.close()
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)
    return jsonify(all_precipitation)

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(station.station).all()
    session.close()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

#Query the dates and temperature observations of the 
#most active station for the last year of data.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date >= '2016-08-23').\
    filter(measurement.date <= '2017-08-23').\
    order_by(measurement.date).all()
    session.close()
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)

#Return a JSON list of the minimum temperature, 
#the average temperature, and the max temperature for 
#a given start or start-end range.
@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
    filter(measurement.date >= start).all()
    session.close()
    all_start = list(np.ravel(results))
    return jsonify(all_start)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
    filter(measurement.date >= start).\
    filter(measurement.date <= end).all()
    session.close()
    all_start_end = list(np.ravel(results))
    return jsonify(all_start_end)

if __name__ == '__main__':
    app.run(debug=True)