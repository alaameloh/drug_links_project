WITH TRANSACTIONS_PRODUCT_TYPE AS (
  SELECT
    trans.client_id AS client_id,
    prod_nom.product_type AS product_type,
    SUM(trans.prod_price*trans.prod_qty) AS total_ventes
  FROM
    TRANSACTION trans
  INNER JOIN
    PRODUCT_NOMENCLATURE prod_nom
  ON
    trans.prop_id = prod_nom.product_id
  WHERE
    date BETWEEN "2019-01-01" AND "2019-12-31"
  GROUP BY
    trans.client_id,
    prod_nom.product_type )


SELECT
  *
FROM
  TRANSACTIONS_PRODUCT_TYPE
PIVOT(
  sum(total_ventes) AS ventes
  FOR product_type IN ("MEUBLE", "DECO")
);
