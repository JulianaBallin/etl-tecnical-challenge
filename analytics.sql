-- 1. top 5 produtos por receita no ultimo ano completo
SELECT 
    dp.product_name,
    SUM(fs.total_price) AS total_revenue
FROM mart.fact_sales fs
JOIN mart.dim_product dp ON fs.product_id = dp.product_id
JOIN mart.dim_date dd ON fs.date_id = dd.date_id
WHERE dd.year = EXTRACT(YEAR FROM CURRENT_DATE) - 1
GROUP BY dp.product_name
ORDER BY total_revenue DESC
LIMIT 5;


-- 2. evolucao mensal de vendas (quantidade e receita) em 2024
SELECT 
    dd.month,
    dd.month_name,
    SUM(fs.quantity) AS total_quantity,
    SUM(fs.total_price) AS total_revenue
FROM mart.fact_sales fs
JOIN mart.dim_date dd ON fs.date_id = dd.date_id
WHERE dd.year = 2024
GROUP BY dd.month, dd.month_name
ORDER BY dd.month;


-- 3. clientes que compraram mais de 10 unidades em uma unica transacao
SELECT 
    account_id,
    product_id,
    date_id,
    quantity
FROM mart.fact_sales
WHERE quantity > 10;


-- 4. receita media por cliente agrupada por estado
SELECT 
    da.state,
    ROUND(AVG(cliente.total_cliente), 2) AS receita_media_por_cliente
FROM (
    SELECT 
        account_id,
        SUM(total_price) AS total_cliente
    FROM mart.fact_sales
    GROUP BY account_id
) cliente
JOIN mart.dim_account da ON cliente.account_id = da.account_id
GROUP BY da.state
ORDER BY receita_media_por_cliente DESC;


-- 5. percentual de crescimento de receita mes a mes nos ultimos 12 meses
WITH receita_por_mes AS (
    SELECT 
        dd.year,
        dd.month,
        DATE_TRUNC('month', dd.date_id) AS mes,
        SUM(fs.total_price) AS receita_mensal
    FROM mart.fact_sales fs
    JOIN mart.dim_date dd ON fs.date_id = dd.date_id
    GROUP BY dd.year, dd.month, mes
    ORDER BY mes
),
crescimento AS (
    SELECT 
        mes,
        receita_mensal,
        LAG(receita_mensal) OVER (ORDER BY mes) AS receita_mes_anterior
    FROM receita_por_mes
)
SELECT 
    mes,
    receita_mensal,
    receita_mes_anterior,
    ROUND(
        CASE 
            WHEN receita_mes_anterior = 0 THEN NULL
            ELSE (receita_mensal - receita_mes_anterior) / receita_mes_anterior * 100
        END, 2
    ) AS crescimento_percentual
FROM crescimento
WHERE mes >= CURRENT_DATE - INTERVAL '12 months';
