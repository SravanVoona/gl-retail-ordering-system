import pymongo
import uuid

def create_mongo_db (db_name, client):
    db_list = client.list_database_names()
    if db_name not in db_list:
        client[db_name]
        
def create_mongo_collection (db_name, collection_name, client):
    db_list = client.list_database_names()
    if db_name not in db_list:
        return
    db_conn = client[db_name]
    col_list = db_conn.list_collection_names()
    if collection_name not in col_list:
        db_conn[collection_name]
        
        
def check_open_auction (product_id, db_conn):
    aution_count = db_conn.auction.count_documents({'product_id': product_id, 'status': 'open'})
    return aution_count

def highest_bidding_amount(auction_id, db_conn):
    max_value_cur = db_conn.bidding.find({'auction_id': auction_id}).sort("bid_amount", -1).limit(1)
    for record in max_value_cur:
        if 'bid_amount' in record:
            return record['bid_amount']
        else:
            return -1
    return -1

def highest_bidding_user(auction_id, db_conn):
    max_value_cur = db_conn.bidding.find({'auction_id': auction_id}).sort("bid_amount", -1).limit(1)
    user_info = dict()
    for record in max_value_cur:
        if 'user_id' in record:
            user_info['user_id'] = record['user_id']
            user_info['bid_amount'] = record['bid_amount']
            return user_info
    return

def extract_auction_info(product_id, db_conn):
    #print(product_id)
    #print(check_open_auction(product_id, db_conn))
    auction_info = db_conn.auction.find({'product_id': product_id, 'status': 'open'})
    auction_dic = dict()
    for row in auction_info:
        auction_dic = dict(row)
        current_max_bid = highest_bidding_amount(auction_dic['auction_id'], db_conn)
        auction_dic['current_max_bid'] = current_max_bid if current_max_bid > 0 else auction_dic['min_amount']
    return auction_dic


def extract_auction_products(db_conn):
    auction_info = db_conn.auction.find({'status': 'open'})
    products_list = []
    for auction_record in auction_info:
        products_list.append(auction_record['product_id'])
    return products_list
    
    

def add_auction(product_id, seller_id, min_amount, increment, start_time, end_time, db_conn):
    if check_open_auction(product_id, db_conn) > 0:
        return 'Auction Already Exists'
    # get a new auction id
    auction_id = str(uuid.uuid4())
    auction = db_conn.auction.insert_one({'auction_id': auction_id,
                                          'product_id': product_id, 
                                          'status': 'open',
                                          'seller_id': seller_id,
                                          'min_amount': min_amount,
                                          'increment': increment,
                                          'start_time': start_time,
                                          'end_time': end_time})
    return 'Auction Created'

def add_bid(auction_id, product_id, user_id, bid_amount, timestamp, db_conn):
    # get auction_id
    if auction_id is None:
        auction_info = extract_auction_info(product_id, db_conn)
        auction_id = auction_info["auction_id"] if auction_info is not None else None
    
    #print(auction_id)  
    # return error if input data is not sufficient 
    if auction_id is None or user_id is None:
        return "Missing or Incorrect Data Sent"
    
    # get the higest bid
    max_bid = highest_bidding_amount(auction_id, db_conn)
    #print(max_bid)
    
    # if bid_amount < max 
    if bid_amount <= max_bid:
        return 'Bid below current max bid amount'
    
    # get a new bid id
    bidding_id = str(uuid.uuid4())
    
    bid = db_conn.bidding.insert_one({'bidding_id': bidding_id,
                                      'auction_id': auction_id,
                                      'user_id': user_id,
                                      'bid_amount': bid_amount,
                                      'timestamp': timestamp})

    return 'Bid Created'


def extract_end_auction(timestamp, db_conn):
    auction_info = db_conn.auction.find({'status': 'open', 'end_time':{'$lt' : timestamp}})
    end_auction_list = []
    for record in auction_info:
        end_auction_list.append(record['auction_id'])
    return end_auction_list

def close_auction(auction_id, user_id, final_price, db_conn):
    # filter condition
    filter = { 'auction_id': auction_id }
    # Values to be updated.
    newvalues = { "$set": { 'status': 'close', 'winning_user': user_id, 'final_price': final_price } }
    # close the auction
    db_conn.auction.update_one(filter, newvalues)
    
    
def extract_user_bids (user_id, db_conn):
    bids = db_conn.bidding.find({'user_id': user_id})
    auction_info_dict = dict()
    user_bids = []
    for bid in bids:
        print(bid['auction_id'])
        bid_dict = dict()
        bid_dict['bidding_id'] = bid['bidding_id']
        bid_dict['auction_id'] = bid['auction_id']
        bid_dict['bid_amount'] = bid['bid_amount']
        bid_dict['timestamp'] = bid['timestamp']
        if bid['auction_id'] not in auction_info_dict:
            auction_info = db_conn.auction.find({'auction_id': bid['auction_id']}).limit(1)
            for auction in auction_info:
                auction_info_dict[auction['auction_id']] = auction
        bid_dict['product_id'] = auction_info_dict[bid['auction_id']]['product_id']
        bid_dict['seller_id'] = auction_info_dict[bid['auction_id']]['seller_id']
        user_bids.append(bid_dict) 
        
    return sorted(user_bids, key=lambda x: x['timestamp'], reverse=True)
            
        
        
        
        
    
    
        
    





    
    
    
    
   


    
    
    
