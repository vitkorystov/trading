CREATE DATABASE trading;

-- таблица с котировками для фьючерсов
CREATE TABLE futures (
    id serial primary key,
    ticker int,
    timeframe int,
    date timestamp,
    open real,
    high real,
    low real,
    close real,
    volume real,
    UNIQUE (ticker, timeframe, date)
);

-- таблица тикеров
CREATE TABLE tickers (
    id serial primary key,
    name text,
    full_name text,
    description text,
    UNIQUE (name, full_name)
);

-- таблица таймфреймов
CREATE TABLE timeframes (
   id serial primary key,
   timeframe varchar (50) UNIQUE
);