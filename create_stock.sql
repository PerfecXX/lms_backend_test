CREATE TABLE stock(
   PDS_KB_NO VARCHAR(22) NOT NULL PRIMARY KEY
  ,PART_NO   VARCHAR(14) NOT NULL
  ,PART_NAME VARCHAR(40) NOT NULL
  ,AMOUT 	 VARCHAR(100) NOT NULL
);
select * from lms.stock