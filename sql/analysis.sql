-- DuckDB views over validated period-grain observations.
CREATE OR REPLACE VIEW summary AS
SELECT count(*) AS records, avg(system_price) AS mean_price,
       median(system_price) AS median_price, min(system_price) AS minimum_price,
       max(system_price) AS maximum_price, max(abs(niv)) AS maximum_absolute_niv,
       count(*) FILTER (WHERE system_length='Short') AS short_periods,
       count(*) FILTER (WHERE system_length='Long') AS long_periods,
       count(*) FILTER (WHERE is_exception) AS exception_periods
FROM settlement;

CREATE OR REPLACE VIEW daily_summary AS
SELECT settlement_date, count(*) AS periods, avg(system_price) AS mean_price,
       median(system_price) AS median_price, min(system_price) AS minimum_price,
       max(system_price) AS maximum_price, avg(abs(niv)) AS mean_absolute_niv,
       count(*) FILTER (WHERE is_exception) AS exceptions
FROM settlement GROUP BY settlement_date ORDER BY settlement_date;

-- SP indices after the clock change do not have a universal local clock label.
CREATE OR REPLACE VIEW period_summary AS
SELECT settlement_period, count(*) AS periods, avg(system_price) AS mean_price,
       median(system_price) AS median_price, avg(niv) AS mean_niv
FROM settlement GROUP BY settlement_period ORDER BY settlement_period;

CREATE OR REPLACE VIEW length_summary AS
SELECT system_length, count(*) AS periods, avg(system_price) AS mean_price,
       median(system_price) AS median_price, stddev_samp(system_price) AS price_stddev,
       quantile_cont(system_price,.05) AS price_p05,
       quantile_cont(system_price,.95) AS price_p95,
       min(system_price) AS minimum_price, max(system_price) AS maximum_price,
       avg(abs(niv)) AS mean_absolute_niv
FROM settlement GROUP BY system_length ORDER BY system_length;

CREATE OR REPLACE VIEW extreme_periods AS
WITH ranked AS (
    SELECT *, rank() OVER(ORDER BY system_price DESC) AS high_price_rank,
              rank() OVER(ORDER BY system_price ASC) AS low_price_rank,
              rank() OVER(ORDER BY abs(niv) DESC) AS imbalance_rank
    FROM settlement
)
SELECT event_id,settlement_date,settlement_period,system_price,niv,system_length,
       high_price_rank,low_price_rank,imbalance_rank,reason_flagged
FROM ranked WHERE high_price_rank<=10 OR low_price_rank<=10 OR imbalance_rank<=10
ORDER BY high_price_rank,settlement_date,settlement_period;

CREATE OR REPLACE VIEW exception_queue AS
SELECT event_id,settlement_date,settlement_period,system_length,niv,system_price,
       price_percentile,niv_percentile,reason_flagged,severity,quality_status
FROM settlement WHERE is_exception
ORDER BY greatest(abs(price_robust_z),niv_percentile/100) DESC,settlement_date,settlement_period;

CREATE OR REPLACE VIEW duplicate_keys AS
SELECT settlement_date,settlement_period,count(*) AS copies
FROM settlement GROUP BY settlement_date,settlement_period HAVING count(*)>1;
