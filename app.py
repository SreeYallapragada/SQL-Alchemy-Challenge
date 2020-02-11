import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

###############################
# Db Setup
###############################
engine = create_engine("sqlite:///data/hawaii.sqlite")

#existing db into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

################################
# Flask Setup
################################

app = Flask(__name__)

################################
# Routes
################################

@app.route("/")
def home_page():
    """List all routes that are available"""
    return (
        f"Thinking of going to Hawaii? Check out the available routes to see the weather there!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    last_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=366)
    # Perform a query to retrieve the data and precipitation scores
    precip_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year_date).all()

    precipitation_dict = {}
    for precipitation in precip_data:
        precipitation_dict[precipitation[0]] = precipitation[1]

    return jsonify(precipitation_dict)


@app.route("/api/v1.0/stations")
def stations():

    most_active_stations = session.query((Station.station)).all()
    stations = list(np.ravel(most_active_stations))
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    last_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=366)
    station_519281 = session.query(Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= last_year_date).order_by(Measurement.date.desc()).all()
    tobs = list(np.ravel(station_519281))
    return jsonify(tobs)


@app.route("/api/v1.0/<start>")
# def start(start):
    
#     result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
#     start_dates = list(np.ravel(result))
#     return jsonify(start_dates)


@app.route("/api/v1.0/<start>/<end>")
def start_date(start = None, end = None):
    if not end: 
        result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
        start_dates = list(np.ravel(result))
    
        return jsonify(start_dates)
    
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    start_dates = list(np.ravel(result))
    return jsonify(start_dates)


if __name__ == "__main__":
    app.run(debug=True)