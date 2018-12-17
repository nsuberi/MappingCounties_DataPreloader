####
## Import required libraries
####

import requests

import psycopg2 as pg
from census import Census
import logging
import sys

from sqlalchemy import create_engine
# https://stackoverflow.com/questions/23103962/how-to-write-dataframe-to-postgres-table?fbclid=IwAR0Unovxw4M_yTfd2rN36XNSzPs6sQQM5em4RJE9tPdfTeNSXga0rFTGoas

LOG_LEVEL = logging.DEBUG
logging.basicConfig(stream=sys.stderr, level=LOG_LEVEL)

####
## Load OSM data for target county
####

# Anne Arundel County
#https://www.openstreetmap.org/relation/936313
# Overpass API
#https://towardsdatascience.com/loading-data-from-openstreetmap-with-python-and-the-overpass-api-513882a27fd0
def load_OSM_data_for_county(COUNTY_RELATION_ID):

    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json];
    relation({});
    out;
    """.format(COUNTY_RELATION_ID)
    response = requests.get(overpass_url,
                            params={'data': overpass_query})
    osm_data = response.json()
    logging.debug('Length of response: {}'.format(len(osm_data)))

    return osm_data

####
## Load Census Data
####

def load_census_data():

    # Load census data
    # https://github.com/datamade/census?fbclid=IwAR37xnYy_SQzi2RwzauZdKbAZV6ZD-xgGhYhq11QjXq3O_WIOsi7k-vmZHs

    c = Census('CENSUS_API_KEY')

    return []

####
## Connect to Postgres database and input data
####

def connect_to_pg(user, password, host, port, database):
    #conn = psychopg2.connect(CONN_STRING)
    engine = create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'.format(user, password, host, port, database))
    conn = engine.raw_connection()
    cur = conn.cursor()
    # SQL Alchemy intro
    # https://www.compose.com/articles/using-postgresql-through-sqlalchemy/
    return cur

def load_data_to_pg(pg_connection, data):
    pass


def main():

    logging.info('Connecting to Postgres DB')
    #pg = connect_to_pg("dbname=colouring_london user=admin")
    pg = connect_to_pg('admin', 'password', 'db', 5432, 'colouring_aac')
    pg.execute("SELECT * FROM information_schema.tables;")
    table = pg.fetchone()
    logging.info('All tables in DB: {}'.format(table))

    logging.info('Loading OSM for Anne Arundel County')
    # https://www.openstreetmap.org/relation/936313
    # Eventually - how to get data from a bounding box: https://wiki.openstreetmap.org/wiki/Overpass_API/Advanced_examples
    osm = load_OSM_data_for_county(936313)
    logging.debug("OSM results: {}".format(osm))

    # logging.info('Loading Census data for Anne Arundel County')
    # census = load_census_data()

    # logging.info('Uploading data to DB')
    # load_data_to_pg(pg, osm)
    # load_data_to_pg(pg, census)

    # logging.info('All Loaded!')
