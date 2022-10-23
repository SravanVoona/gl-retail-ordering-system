from xmlrpc.client import ProtocolError
from pymongo import MongoClient
from flask import Flask
from bson.json_util import dumps
import yaml

yaml_config = yaml.safe_load(open('config.yaml'))

DATABASE_NAME = yaml_config['mongodb']['database'] 
TABLE_ONE = yaml_config['mongodb']['tables'][0] 
TABLE_TWO = yaml_config['mongodb']['tables'][1] 

### Flask App ###
app = Flask(__name__)  

### Create Mongo Client ###
mongo_client = MongoClient(yaml_config['mongodb']['connection_string'])

### Create Mongo database object ###
mongo_db_conn = mongo_client[DATABASE_NAME]

from src import routes
from src import models


### Set up database ###
models.create_mongo_collection(DATABASE_NAME, TABLE_ONE, mongo_client) 
models.create_mongo_collection(DATABASE_NAME, TABLE_TWO, mongo_client) 


