WITH input_data AS (
	SELECT 50 AS long_ma_n,
		   5 AS short_ma_n,
		   50 AS take_profit,
	       'Si-12.20' AS ticker
), 

t1 AS (
	SELECT 
		date, open, high, low, close,
		avg(close) OVER (ORDER BY date ROWS BETWEEN (SELECT long_ma_n-1 FROM input_data) PRECEDING AND CURRENT ROW) as ma_long,
		avg(close) OVER (ORDER BY date ROWS BETWEEN (SELECT short_ma_n-1 FROM input_data) PRECEDING AND CURRENT ROW) as ma_short
	FROM futures
	WHERE ticker = (SELECT id FROM tickers WHERE full_name=(SELECT ticker FROM input_data))
	ORDER BY date
), 

t2 AS ( 
	SELECT  
		date, open, high, low, close,	
		ma_long, ma_short,
	    -- предыдущие значения MA
		LAG(ma_long, 1) OVER (ORDER BY date) as prev_ma_long,		
		LAG(ma_short, 1) OVER (ORDER BY date) as prev_ma_short
	FROM t1
),

t3 AS (
	SELECT 
		date AS start_deal_date,                           -- дата начала сделки
	    open, high, low, close, ma_long, ma_short,
	    LEAD(date) OVER(ORDER BY date) AS end_deal_date,   -- дата окончания сделки
        -- точки пересечения
		CASE 
			WHEN (ma_short > ma_long AND prev_ma_short < prev_ma_long) THEN 'buy'
			WHEN (ma_short < ma_long AND prev_ma_short > prev_ma_long) THEN 'sell'
		END AS cross_type, 
		close AS start_deal_price,                          -- цена открытия сделки
	    LEAD(close) OVER(ORDER BY date) AS end_deal_price   -- цена закрытия сделки
	FROM t2
	WHERE (ma_short > ma_long AND prev_ma_short < prev_ma_long) 
		   OR
		  (ma_short < ma_long AND prev_ma_short > prev_ma_long)	
), 

t4 AS (
	SELECT 
		*,
	    -- цена, при которой будет максимальная потенциальная прибыль в сделке
		CASE 
			WHEN cross_type = 'buy'
				THEN (SELECT max(high) FROM futures WHERE date BETWEEN start_deal_date AND end_deal_date AND ticker = (SELECT id FROM tickers WHERE full_name=(SELECT ticker FROM input_data)))
			WHEN cross_type = 'sell'
				THEN (SELECT min(low) FROM futures WHERE date BETWEEN start_deal_date AND end_deal_date AND ticker = (SELECT id FROM tickers WHERE full_name=(SELECT ticker FROM input_data)))
		END AS peak_price,
	    -- продолжительность сделки в барах
		(SELECT count(open) FROM futures WHERE date BETWEEN start_deal_date AND end_deal_date AND ticker = (SELECT id FROM tickers WHERE full_name=(SELECT ticker FROM input_data))) AS duration
	FROM t3
),

t5 AS (
	SELECT 
		*,
	    -- максимальная потенциальная прибыль
		CASE
			WHEN cross_type = 'buy'
				THEN peak_price - start_deal_price
			WHEN cross_type = 'sell'
				THEN start_deal_price - peak_price
		END AS max_delta,
		CASE
			WHEN cross_type = 'buy'
				THEN end_deal_price - start_deal_price
			WHEN cross_type = 'sell'
				THEN start_deal_price - end_deal_price
		END AS direct_deal_res	
	FROM t4
),

t6 AS (
	SELECT *,
        -- прибыль сделки если применять take_profit
		CASE
			WHEN max_delta > (SELECT take_profit FROM input_data) THEN (SELECT take_profit FROM input_data)
			ELSE direct_deal_res
		END AS with_take_profit	
	FROM t5
)

--SELECT * FROM t6 --WHERE with_take_profit>0

SELECT 
	sum(direct_deal_res) as direct_deal_res_sum,
	sum(with_take_profit) as with_take_profit_sum,
	count(direct_deal_res) as deal_count,
	count(direct_deal_res)*2.13 as comm,  -- комиссия*/
    (SELECT count(*) FROM t6 WHERE direct_deal_res>0) as pos_deals_direct,
    (SELECT count(*) FROM t6 WHERE direct_deal_res<0) as neg_deals_direct,
    (SELECT count(*) FROM t6 WHERE with_take_profit>0) as pos_deals_tp,
    (SELECT count(*) FROM t6 WHERE with_take_profit<0) as neg_deals_tp
FROM t6



