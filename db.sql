drop table stock.INFO;

CREATE TABLE stock.INFO (
  serial INT(16) UNSIGNED AUTO_INCREMENT NOT NULL COMMENT '번호',
  exchanger VARCHAR(64) NOT NULL COMMENT '거래소',   
  date DATETIME NOT NULL COMMENT '등록일',  
  currency VARCHAR(64) NOT NULL COMMENT '통화',   
  errorCode VARCHAR(64) COMMENT 'errcode',  
  result VARCHAR(64) COMMENT '결과',  
  first INT(16) COMMENT 'first',
  high INT(16) COMMENT 'high',
  last INT(16) COMMENT 'last',
  low INT(16) COMMENT 'low',
  yesterday_first INT(16) COMMENT 'yesterday_first',
  yesterday_high INT(16) COMMENT 'yesterday_high',
  yesterday_last INT(16) COMMENT 'yesterday_last',
  yesterday_low INT(16) COMMENT 'yesterday_low',  
  volume DOUBLE COMMENT 'volume',
  yesterday_volume DOUBLE COMMENT 'yesterday_volume',
  timestamp INT(64) COMMENT 'timestamp',  
  sma_5 DOUBLE COMMENT 'sma_5',
  sma_15 DOUBLE COMMENT 'sma_15',
  sma_50 DOUBLE COMMENT 'sma_50',    
  volume_rate FLOAT COMMENT 'volume rate',
  
  PRIMARY KEY (serial),    
  INDEX (exchanger, date, currency)  
) COMMENT = 'info' ROW_FORMAT = DEFAULT CHARACTER SET utf8 ENGINE=InnoDB;

drop table stock.STOCK_SIGNAL;

CREATE TABLE stock.STOCK_SIGNAL (
  signal_serial INT(16) UNSIGNED AUTO_INCREMENT NOT NULL COMMENT '번호',
  exchanger VARCHAR(64) NOT NULL COMMENT '거래소',   
  date DATETIME NOT NULL COMMENT '등록일',  
  currency VARCHAR(64) NOT NULL COMMENT '통화', 
         
  up_cross INT(8) NOT NULL default 0 COMMENT 'up cross signal',
  down_cross INT(8)  NOT NULL default 0 COMMENT 'down cross signal',
  up_50_cross INT(8)  NOT NULL default 0 COMMENT 'up cross 50 signal',
  down_50_cross INT(8)  NOT NULL default 0 COMMENT 'down cross 50 signal',
  volume_signal INT(8)  NOT NULL default 0 COMMENT 'volume signal',  
  
  PRIMARY KEY (signal_serial),
  INDEX (exchanger, date, currency)    
) COMMENT = 'STOCK_SIGNAL' ROW_FORMAT = DEFAULT CHARACTER SET utf8 ENGINE=InnoDB;

drop table stock.ORDERS;

CREATE TABLE stock.ORDERS (
  order_serial INT(16) UNSIGNED AUTO_INCREMENT NOT NULL COMMENT '번호', 
  exchanger VARCHAR(64) NOT NULL COMMENT '거래소',
  date DATETIME NOT NULL COMMENT '등록일',  
  currency VARCHAR(64) NOT NULL COMMENT '통화',          
  type varchar(64) NOT NULL COMMENT 'bid or ask',
  price int(16) NOT NULL comment 'price',  
  qty   float not null comment 'quentity',
  feeRate float not null comment 'fee rate',
  fee float not null comment 'fee',
  order_id varchar(256) not null comment 'corder id',    
  profit double NOT NULL default 0 comment 'profit',
  PRIMARY KEY (order_serial),
  INDEX ( exchanger, date, currency),
  INDEX (order_id)
) COMMENT = 'ORDERS' ROW_FORMAT = DEFAULT CHARACTER SET utf8 ENGINE=InnoDB;

drop table stock.TEST;

CREATE TABLE stock.TEST (
  test_serial INT(16) UNSIGNED AUTO_INCREMENT NOT NULL COMMENT '번호', 
  exchanger VARCHAR(64) NOT NULL COMMENT '거래소',    
  date DATETIME NOT NULL COMMENT '등록일',  
  currency VARCHAR(64) NOT NULL COMMENT '통화',          
  type varchar(64) NOT NULL COMMENT 'bid or ask',
  price int(16) NOT NULL comment 'price',  
  qty   float not null comment 'quentity',
  feeRate float not null comment 'fee rate',
  fee float not null comment 'fee',
  order_id varchar(256) not null comment 'corder id',    
  profit double NOT NULL default 0 comment 'profit krw',
  balance double NOT NULL default 0 comment 'balance krw',
  crypto_balance double NOT NULL default 0 comment 'balance cryptocurrency',
  PRIMARY KEY (test_serial),
  INDEX ( exchanger, date, currency),
  INDEX (order_id)
) COMMENT = 'TEST' ROW_FORMAT = DEFAULT CHARACTER SET utf8 ENGINE=InnoDB;
