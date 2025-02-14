#from xmlrpc.client import ProtocolError
from pymongo import MongoClient
from flask import Flask
#from bson.json_util import dumps
from src import app
from src import mongo_db_conn

from src import models
import yaml
from flask import jsonify
from flask import request
from datetime import datetime

yaml_config = yaml.safe_load(open('config.yaml'))
DATABASE_NAME = yaml_config['mongodb']['database'] 



@app.route("/")
def home():
    return "Running Bidding Service"


@app.route("/create_auction", methods = ['POST'])
def create_auction():
  try:
    payload = request.get_json()
    seller_id = int(payload["sellerId"])
    product_id  = int(payload["productId"])
    min_amount = float(payload["min_amount"])
    if 'increment' in payload:
      increment = float(payload["increment"])
    else:
      increment = min_amount*0.1
    start_time = (payload["start_time"])
    end_time = (payload["start_time"])
    return jsonify(models.add_auction(product_id, seller_id, min_amount, increment, start_time, end_time, mongo_db_conn))
  except Exception as e:
    return jsonify({"status": 400, "err": str(e)})
  

@app.route("/create_bid", methods = ['POST'])
def create_bid():
  try:
    payload = request.get_json()
    
    if "auctionId" in payload:
      auction_id = str(payload["auctionId"])
    else:
      auction_id = None
    
    if "productId" in payload:
      product_id = int(payload["productId"])
    else:
      product_id = None
    userId  = int(payload["userId"])
    bid_amount = float(payload["bidAmount"])
    if "timestamp" in payload:
      timestamp = (payload["timestamp"])
    else:
      timestamp = datetime.now().isoformat(sep='T',timespec='auto') # get Current datetime
    return jsonify(models.add_bid(auction_id, product_id, userId, bid_amount, timestamp, mongo_db_conn))
  except Exception as e:
    return jsonify({"status": 400, "err": str(e)})
  
@app.route("/auction_products", methods = ['GET'])
def get_auction_products():
  try:
    auction_products = models.extract_auction_products(mongo_db_conn)
    return jsonify(auction_products)
  except Exception as e:
    return jsonify({"status": 400, "err": str(e)})

  
@app.route("/auction", methods = ['GET'])
def get_auction():
  try:
    product_id = int(request.args.get('productId'))
    auction_info = models.extract_auction_info(product_id, mongo_db_conn)
    if auction_info:
      auction_info.pop('_id')
    return jsonify(auction_info)
  except Exception as e:
    return jsonify({"api_status": 400, "err": str(e)})
  
@app.route("/user_bids", methods = ['GET'])
def get_user_bids():
  try:
    user_id = int(request.args.get('userId'))
    return jsonify(models.extract_user_bids(user_id, mongo_db_conn))
  except Exception as e:
    return jsonify({"status": 400, "err": str(e)})
  

    
    


