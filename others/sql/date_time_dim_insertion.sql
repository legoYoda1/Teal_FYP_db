-- Set a higher limit just for this session
SET SESSION cte_max_recursion_depth = 20000;

INSERT INTO date_dim (date_id, day, month, year)
WITH RECURSIVE date_series (date) AS (
  SELECT DATE('2000-01-01')
  UNION ALL
  SELECT DATE_ADD(date, INTERVAL 1 DAY)
  FROM date_series
  WHERE date < '2050-12-31'
)
SELECT
    CAST(DATE_FORMAT(date, '%d%m%Y') AS UNSIGNED) AS date_id,
    DAY(date) AS day,
    MONTH(date) AS month,
    YEAR(date) AS year
FROM date_series;