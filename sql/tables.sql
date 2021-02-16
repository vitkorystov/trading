CREATE DATABASE trading;


CREATE TABLE futures (
    id serial primary key,
    ticker int,
    timeframe varchar (50),
    date timestamp,
    open real,
    high real,
    low real,
    close real,
    volume real,
    UNIQUE (ticker, timeframe, date)
);

CREATE TABLE tickers (
    id serial primary key,
    name text,
    full_name text,
    description text
)

CREATE TABLE timeframes (
   id serial primary key,
   timeframe varchar (50) UNIQUE
)

INSERT INTO
	timeframes (timeframe)
VALUES
	('1m'), ('5m'),	('10m'), ('15m'), ('30m'),
	('1h'), ('4h'),
	('1d'), ('1w'), ('1mo');
