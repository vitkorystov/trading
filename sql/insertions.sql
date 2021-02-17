INSERT INTO
    timeframes (timeframe)
VALUES
('1m'), ('5m'),	('10m'), ('15m'), ('30m'),
('1h'), ('4h'),
('1d'), ('1w'), ('1mo')
ON CONFLICT(timeframe) DO NOTHING;


INSERT INTO tickers (name, full_name, description)
VALUES ('SiH1', 'Si-3.21', 'US-RUB futures with exp data at 03.21')
ON CONFLICT(name, full_name) DO NOTHING RETURNING id;


