use regalia

alter table cart add column bidprice decimal(10,0);

alter table ordered_details add column status varchar(100);

alter table sale_transaction drop column amount;
alter table sale_transaction drop column cc_number;
alter table sale_transaction drop column cc_type;
alter table sale_transaction add column razorpay_id varchar(100);