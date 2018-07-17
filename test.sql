select date, last, sma_5, sma_10, volume, volume_rate from INFO where currency='xrp' order by serial asc limit 100;

-- select A.*, sma_5, sma_10, sma_15 from STOCK_SIGNAL A, INFO B 
-- where A.currency='xrp' and A.date >= '2018-01-02 14:42:16' and A.currency = B.currency and A.`date` = B.`date`
-- select * from STOCK_SIGNAL where currency='xrp' and down_cross = 1