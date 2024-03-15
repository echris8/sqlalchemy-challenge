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
#db_string = "Resources/hawaii.sqlite"
#engine = create_engine(f"sqlite:///{db_string}")

engine = create_engine("sqlite:///C:/Users/enc308/OneDrive - Northwestern University/Documents/Data Science/NU-VIRT-DATA-PT-10-2023-U-LOLC/02-Homework/10-Advanced-SQL/Instructions/Starter_Code/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine, reflect=True)

# Save references to each table
measurement = Base.classes['measurement']
station = Base.classes["station"]

# Create our session (link) from Python to the DB
session = Session(engine)

''''
# Print table names
print("Tables:")
for table_name in Base.metadata.tables.keys():
    print(table_name)

# Print data from each table
for table_name in Base.metadata.tables.keys():
    print(f"Data from table: {table_name}")
    table_data = session.query(Base.classes[table_name]).all()
    for row in table_data:
        print(row)
'''

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#Find the most recent year and one year from date as needed for other pages
def date_prev_year():
    most_recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()

    if most_recent_date:
        most_recent_date = most_recent_date[0]
        most_recent_date = dt.datetime.strptime(most_recent_date, "%Y-%m-%d").date()
        one_year_ago = most_recent_date - dt.timedelta(days=365)
        return most_recent_date, one_year_ago
    else:
        return None, None

most_recent_date, one_year_ago = date_prev_year()

#################################################
# Flask Routes
#################################################

#homepage
@app.route("/")
def welcome():
    return """
       Welcome to the Hawaii Weather API!<br/>
        Possible Routes:<br/>
       <ol>
       <li><a href="/api/v1.0/precipitation">Precipitation</a></li>
       <li><a href="/api/v1.0/stations">Stations</a></li>
       <li><a href="/api/v1.0/tobs">Temperature Observations</a></li>
       <li><a href="/api/v1.0/start_date">Start Date</a></li>
       When you click this link, edit the URL where it says 'start_date' to have your date of travel.<br/>
       <li><a href="/api/v1.0/start_date/end_date">Date Range</a></li>
       When you click this link, edit where the URL shows 'start_date' and 'end_date to include the start date and end date of your trip.<br/>
       <br/>
       All dates should be in the format of YYYY-MM-DD.<br/>
      </ol>
  """

# /api/v1.0/precipitation page
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create the session
    session = Session(engine)

    # Pull precipitation data from last year
    most_recent_date, one_year_ago = date_prev_year()
    prcp_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_ago).all()

    # Using a loop to create a list of dictionaries
    prcp_list = [{"date": date, "prcp": prcp} for date, prcp in prcp_data]

    session.close()

    if not prcp_list:
        return jsonify({"error": "No data found."}), 404

    return jsonify(prcp_list)

# /api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    # Create the session
    session = Session(engine)

    # Query station data from the Station dataset
    station_data = session.query(station.station).all()

    # Close the session
    session.close()

    # Convert Row objects to dictionaries
    station_list = [{"station": row.station} for row in station_data]

    return jsonify(station_list)

 #/api/v1.0/tob
@app.route("/api/v1.0/tobs")
def tobs():
    # Identify the most active station
    most_active_station = session.query(measurement.station, func.count(measurement.station)).\
        group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).first()[0]

    # Find the most recent year and one year from date
    most_recent_date, one_year_ago = date_prev_year()

    # Query temperature observations for the most active station in the previous year
    tobs_data = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == most_active_station).\
        filter(measurement.date >= one_year_ago).\
        all()

    # Create a list of dictionaries for the JSON response
    tobs_list = [{"date": date, "tobs": tobs} for date, tobs in tobs_data]

    return jsonify(tobs_list)

 #/api/v1.0/<start> 

@app.route("/api/v1.0/<start>")
def startinfo(start):
    """Return a list of the temperature statistics after the provided date"""
    session = Session(engine)
    # Define functions for min, max, and avg
    sel = [measurement.station,
           func.min(measurement.tobs),
           func.max(measurement.tobs),
           func.avg(measurement.tobs)]
    # Query for all temperatures after the provided start date
    temp_start = session.query(*sel).\
                   filter(measurement.date >= start).all()
    session.close()
    # Create empty list
    start_stats = []
    # Append the statistics from the query to the list
    for station, min, max, avg in temp_start:
        start_dict = {}
        start_dict["Station"] = station
        start_dict["Min_Temperature"] = min
        start_dict["Max_Temperature"] = max
        start_dict["Avg_Temperature"] = avg
        start_stats.append(start_dict)
    # Return jsonified statistics
    return jsonify(start_stats)

# /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>/<end>")
def startendinfo(start, end):
    """Return a list of the temperature statistics between the provided dates"""
    session = Session(engine)
    # Define functions for min, max, and avg
    sel = [measurement.station,
           func.min(measurement.tobs),
           func.max(measurement.tobs),
           func.avg(measurement.tobs)]
    # Query for all temperatures between the provided dates
    temp_start_end = session.query(*sel).\
                   filter(measurement.date >= start).\
                   filter(measurement.date <= end).all()
    session.close()
     # Create empty list
    start_end_stats = []
    # Append the statistics from the query to the list
    for station, min, max, avg in temp_start_end:
        start_end_dict = {}
        start_end_dict["Station"] = station
        start_end_dict["Min_Temperature"] = min
        start_end_dict["Max_Temperature"] = max
        start_end_dict["Avg_Temperature"] = avg
        start_end_stats.append(start_end_dict)
    # Return jsonified statistics
    return jsonify(start_end_stats)
#End

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)