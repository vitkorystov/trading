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


INSERT INTO tickers (name, full_name, description)
VALUES ('SiZ0', 'Si-12.20', 'US-RUB futures with exp data at 12.20')
ON CONFLICT(name, full_name) DO NOTHING RETURNING id;

INSERT INTO tickers (name, full_name, description)
VALUES ('SiU0', 'Si-9.20', 'US-RUB futures with exp data at 9.20')
ON CONFLICT(name, full_name) DO NOTHING RETURNING id;

INSERT INTO tickers (name, full_name, description)
VALUES ('SiM0', 'Si-6.20', 'US-RUB futures with exp data at 6.20')
ON CONFLICT(name, full_name) DO NOTHING RETURNING id;

INSERT INTO tickers (name, full_name, description)
VALUES ('SiH0', 'Si-3.20', 'US-RUB futures with exp data at 3.20')
ON CONFLICT(name, full_name) DO NOTHING RETURNING id;

INSERT INTO tickers (name, full_name, description)
VALUES ('SRH1', 'SBRF-3.21', 'Фьючерсный контракт на обыкновенные акции ПАО Сбербанк')
ON CONFLICT(name, full_name) DO NOTHING RETURNING id;

INSERT INTO tickers (name, full_name, description)
VALUES ('SRZ0', 'SBRF-12.20', 'Фьючерсный контракт на обыкновенные акции ПАО Сбербанк')
ON CONFLICT(name, full_name) DO NOTHING RETURNING id;
