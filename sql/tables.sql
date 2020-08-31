CREATE DATABASE trading;


CREATE TABLE futures (
    id serial primary key,
    ticker varchar(100),
    date timestamp,
    open real,
    high real,
    low real,
    close real,
    volume real
);


