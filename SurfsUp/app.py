# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt


#################################################
# Database Setup
#################################################
db_path = "./Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{db_path}")
#engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<h1>Honolulu Climate Analysis API</h1>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Dynamic Route not included :( <br/>"
    )

##############
#precipitation
##############
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create the session
    session = Session(engine)

    # define the year prior to most recent date
    year_minus_mr_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Perform a query to retrieve the data and precipitation scores
    prcp_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_minus_mr_date).all()
    
    # Close the session                   
    session.close()

    # Create a dictionary in a list
    prcp_list = []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    # Return a list of jsonified precipitation data for the previous 12 months 
    return jsonify(prcp_list)

############
#stations
############
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    # Query station data from the Station dataset
    station_data = session.query(station.station).all()

    # Close the session                   
    session.close()

    # Convert list of tuples into normal list
    station_list = [item for tuple in station_data for item in tuple]

    # Return a list of jsonified station data
    return jsonify(station_list)

############
#tobs
############
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # define the year prior to most recent date
    year_minus_mr_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query tobs data from last 12 months from the most recent date from Measurement table
    tobs_data = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').\
                        filter(measurement.date >= year_minus_mr_date).all()

    # Close the session                   
    session.close()

    # Create a dictionary in a list
    tobs_list = []
    for date, tobs in tobs_data:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)

    # Return a list of jsonified tobs data for the previous 12 months
    return jsonify(tobs_list)

######################
#Dynamic Route
#####################


# Define main branch 
if __name__ == "__main__":
    app.run(debug = True)