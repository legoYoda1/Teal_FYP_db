-- Insert rows into the date_dim table for the range 2000-2050
WITH RECURSIVE date_series AS (
    SELECT '2000-01-01' AS date
    UNION ALL
    SELECT date(date, '+1 day') 
    FROM date_series
    WHERE date < '2050-12-31'
)
INSERT INTO date_dim (date_id, day, month, year)
SELECT
    CAST(strftime('%d%m%Y', date) AS INTEGER) AS date_id,  -- Format as 'ddmmyyyy' and cast to integer
    CAST(strftime('%d', date) AS INTEGER) AS day,
    CAST(strftime('%m', date) AS INTEGER) AS month,
    CAST(strftime('%Y', date) AS INTEGER) AS year
FROM date_series;