from pymongo import MongoClient
import models
import yaml
from datetime import datetime
import schedule
import time


### Extract Config Information ###
yaml_config = yaml.safe_load(open("../config.yaml"))

### Extract Database Name ###
DATABASE_NAME = yaml_config['mongodb']['database'] 

### Initiate mongo Client ###
mongo_client = MongoClient(yaml_config['mongodb']['connection_string'])

### Create Mongo Db Objecct ###
mongo_db_conn = mongo_client[DATABASE_NAME]

# get current datetime
current_iso_datetime = datetime.now().isoformat(sep='T',timespec='auto')


def auction_closing(): 
    print("<-- Job Running -->")
    # get ended auctions which are open
    end_auction_info = models.extract_end_auction(current_iso_datetime, mongo_db_conn)
    print(end_auction_info)

    for auction_id in end_auction_info:
        print(auction_id)
        # get winning information
        winning_info = models.highest_bidding_user(auction_id, mongo_db_conn)
        
        if winning_info is None:
            continue
        
        # extract the inforation
        user_id = winning_info['user_id'] if 'user_id' in winning_info else None
        final_amount = winning_info['bid_amount'] if 'bid_amount' in winning_info else None
        
        # Update auction record
        print(auction_id, ' - ', user_id, ' - ', final_amount)
        models.close_auction(auction_id, user_id, final_amount, mongo_db_conn)
        
        
# Task scheduling
# After every 10 mins geeks() is called.
schedule.every(5).seconds.do(auction_closing)


# Loop so that the scheduling task
# keeps on running all time.
while True:
 
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)
        
    
            
    