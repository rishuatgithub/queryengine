SELECT
col1,
col2,
col3,
col4,
col5,
'abc' as sample_field
FROM
db1.tableA as a
LEFT OUTER JOIN
db1.tableB as b 
ON a.col1 = b.col4
WHERE a.col2 = 'ABC'