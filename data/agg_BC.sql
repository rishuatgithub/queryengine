SELECT
*
FROM
db1.fact_AB as a 
INNER JOIN
db1.tableA as b
on a.col1 = b.col1 
INNER JOIN
db1.tableB as c 
on c.col2 = a.col1