import numpy as np
import datetime as dt
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# # Save references to each table
# measurement = Base.classes['measurement']
# station = Base.classes["station"]

# # Create our session (link) from Python to the DB
# session = Session(engine)

# #################################################
# # Flask Setup
# #################################################
# app = Flask(__name__)

# #Find the most recent year and one year from date as needed for other pages
# # Find the most recent year and one year from date as needed for other pages
# def date_prev_year():
#     most_recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()

#     most_recent_date = most_recent_date[0] if most_recent_date else None

#     if most_recent_date:
#         most_recent_date = dt.datetime.strptime(most_recent_date, "%Y-%m-%d").date()
#         one_year_ago = most_recent_date - dt.timedelta(days=365)
#         return most_recent_date, one_year_ago
#     else:
#         return None, None

# most_recent_date, one_year_ago = date_prev_year()

# #################################################
# # Flask Routes
# #################################################

# #homepage
# @app.route("/")
# def welcome():
#     return """
#         Welcome to the Hawaii Weather API!<br/>
#         Possible Routes:<br/>
#         <ol>
#         <li>"/api/v1.0/precipitation<br/>
#         <li>"/api/v1.0/stations<br/>
#         <li>"/api/v1.0/tobs<br/>
#         <li>"/api/v1.0/<start><br/>
#         <li>"/api/v1.0/<start>/<end><br/>
#         </ol>
#     """

# #/api/v1.0/precipitation page 
# @app.route("/api/v1.0/precipitation")
# def precipitation():
#     # Create the session
#     session = Session(engine)

#     #Pull precipitation data from last year
#     prcp_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_ago()).all()

#     # Using a loop to create a list of dictionaries
#     prcp_list = []
#     for date, prcp in prcp_data:
#         prcp_dict = {"date": date, "prcp": prcp}
#         prcp_list.append(prcp_dict)

#     # Using a dictionary comprehension to directly create a dictionary
#     prcp_dict = {date: prcp for date, prcp in prcp_data}

#     session.close

#     if not prcp_list:
#         return jsonify({"error": f"Station not found."}), 404

#     return jsonify(prcp_list)

# #/api/v1.0/stations
# @app.route("/api/v1.0/stations")
# def stations():
#     # Create the session
#     session = Session(engine)

#     # Query station data from the Station dataset
#     station_data = session.query(station.station).all()

#     # Close the session                   
#     session.close()

#     # Return a list of jsonified station data
#     return jsonify(station_data)

# #/api/v1.0/tobs
# #@app.route("/api/v1.0/tobs")
# #def stations():
#     # Create the session 
#     #session = Session(engine)



# #/api/v1.0/<start> & /api/v1.0/<start>/<end>

# if __name__ == '__main__':
#     app.run(debug=True)