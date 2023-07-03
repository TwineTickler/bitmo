SELECT * FROM response_status rs 

CREATE TABLE IF NOT EXISTS response_status_v2 (
                timestamp NUMERIC,
                error_code INTEGER,
                error_message TEXT,
                elapsed INTEGER,
                credit_count INTEGER,
                total_count INTEGER,
                endpoint TEXT,
                insert_date NUMERIC
            )
            
INSERT INTO response_status_v2 
SELECT "timestamp" as "timestamp",
	error_code as error_code ,
	error_message as error_message ,
	elapsed as elapsed ,
	credit_count as credit_count ,
	total_count as total_count ,
	endpoint as endpoint ,
	insert_date as insert_date 
		from response_status 
		
select count(*) from response_status_v2
SELECT count(*) FROM response_status

ALTER TABLE response_status RENAME TO response_status_old
ALTER TABLE response_status_v2 RENAME TO response_status



CREATE TABLE IF NOT EXISTS quote_v2 (
                id INTEGER,
                symbol TEXT,
                currency_base TEXT,
                insert_date NUMERIC,
                price NUMERIC,
                volume_24h NUMERIC,
                volume_change_24h NUMERIC,
                percent_change_1h NUMERIC,
                percent_change_24h NUMERIC,
                percent_change_7d NUMERIC,
                percent_change_30d NUMERIC,
                percent_change_60d NUMERIC,
                percent_change_90d NUMERIC,
                market_cap NUMERIC,
                market_cap_dominance NUMERIC,
                last_updated_cmc NUMERIC,
                cmc_rank INTEGER,
                num_market_pairs INTEGER
            )
            
INSERT INTO quote_v2 
SELECT * FROM quote 

SELECT COUNT(*) FROM quote q 
SELECT COUNT(*) FROM quote_v2 qv 

ALTER TABLE quote RENAME TO quote_old
ALTER TABLE quote_v2 RENAME TO quote