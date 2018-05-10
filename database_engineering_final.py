
# coding: utf-8

# In[55]:


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# SQL Alchemy
from sqlalchemy import create_engine

# PyMySQL 
import pymysql
pymysql.install_as_MySQLdb()

# Imports the methods needed to abstract classes into tables
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Allow us to declare column types
from sqlalchemy import Column, Integer, String, Date, Float 
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# In[56]:


# inport csv data into pandas
hawaiidata = "clean_hawaii2.csv"

hawaii_df = pd.read_csv(hawaiidata)
hawaii_df.head(10)


# In[57]:


engine = create_engine("sqlite:///hawaii.sqlite", echo=False)
Base.metadata.create_all(engine)
session = Session(engine)


# In[58]:


class Measurement(Base):
    __tablename__ = 'measurement_coll'
    id = Column(Integer, primary_key=True)
    station = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    elevation=Column(Float)
    
class Station(Base):
    __tablename__ = 'station_coll'
    id = Column(Integer, primary_key=True)
    station=Column(String(255))
    name=Column(String(255))
    date=Column(Date)
    prcp=Column(Float)
    tobs=Column(Integer)


# In[59]:


get_ipython().system('rm hawaii.sqlite')


# In[60]:


hawaii_df.to_sql(con=engine, name=Measurement.__tablename__, if_exists='append', index_label = "id")


# In[61]:


from sqlalchemy import  inspect
inspector = inspect(engine)
inspector.get_table_names()


# In[62]:


columns = inspector.get_columns('measurement')
for column in columns:
    print(column["name"], column["type"])

Precipitation = Base.classes.measurement_coll
# In[63]:


app = Flask(__name__)


# In[53]:


@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs,<br/>"
        f"/api/v1.0/stations"
        )

@app.route("/api/v1.0/precipitation")
def weath():
    results=session.query(Precipitation.date).all()
    all_rain = list(np.ravel(results))
    return jsonify(all_rain)

@app.route("/api/v1.0/precipitation")
def temp():
    results = session.query(Precipitation.tobs).all()
    all_temp = list(np.ravel(results))
    return jsonify(all_temp)

@app.route("/api/v1.0/stations")
def stations():
    results=session.query(Precipitation.station).all()
    all_stations= list(np.ravel(results))
    return jsonify(all_stations)

    all_weath = []
    for weather in results:
        weather_dict = {}
        weather_dict ["date"] = weather.date
        weather_dict ["tobs"] = weather.tobs
        all_weath.append(weather_dict)
        return jsonify(all_weath)


# In[54]:


if __name__ == '__main__':
    app.run(debug=True)

