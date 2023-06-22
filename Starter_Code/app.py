# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
import numpy as np
import datetime as dt
from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine, reflect=True)
Base.classes.keys()
# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
        f"put all dates in Year-month-day"
    )
@app.route("/api/v1.0/precipitation")
def precip():
    session.query(measurement.date).order_by(measurement.date.desc()).first()
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    Date_PRCP =session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= year_ago).all()
    preciplist = []
    for p in Date_PRCP:
        d = {"date" : p[0], 
        'rain' : p[1]} 
        preciplist.append(d)
        
    print(preciplist)
    return jsonify(preciplist)


@app.route("/api/v1.0/stations")
def stations():

    station2 = session.query(station.station).all()
    stationlist = []
    for s in station2:
        st = {"station": s[0]}
        stationlist.append(st)

    return jsonify(stationlist)
@app.route("/api/v1.0/tobs")
def tobs():
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results3 = session.query(measurement.date, measurement.tobs).\
    filter(measurement.station == "USC00519281").\
    filter(measurement.date >= year_ago).all()
    tempstationlist = []
    for r in results3:
        H = {"date":r[0], "temp":r[1]}
        tempstationlist.append(H)

    return jsonify(tempstationlist)
@app.route("/api/v1.0/<start>")
def start(start):
    start2 = session.query(func.avg(measurement.tobs), func.max(measurement.tobs), func.min(measurement.tobs)).filter(measurement.date >= start ).all()
    start_list = []
    for tart in start2:
        Z = {"Average": tart[0], "Max":tart[1], "Min": tart[2]}
        start_list.append(Z)

    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")
def begin(start,end):
    start2 = session.query(func.avg(measurement.tobs), func.max(measurement.tobs), func.min(measurement.tobs)).filter(measurement.date >= start ).filter(measurement.date <= end ).all()
    start_list = []
    for tart in start2:
        Z = {"Average": tart[0], "Max":tart[1], "Min": tart[2]}
        start_list.append(Z)

    return jsonify(start_list)


        

if __name__ == '__main__':
    app.run(debug=True)
