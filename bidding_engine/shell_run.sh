#!/bin/bash
  
# turn on bash's job control
set -m
  
# Start the primary process and put it in the background
python run.py &
  
# Start the helper process
python "./src/auction_closing.py"
  
# the my_helper_process might need to know how to wait on the
# primary process to start before it does its work and returns
  
  
# now we bring the primary process back into the foreground
# and leave it there
fg %1


# docker image build --tag bidding_engine:1.0 .
# docker run -p 7000:7000 bidding_engine:1.0