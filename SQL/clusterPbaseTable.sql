-- pbaseCluster base construction

CREATE TABLE `stvis`.`pbaseCluster` ( `id` INT NOT NULL AUTO_INCREMENT , `nid` CHAR(18) NOT NULL , `lng` DOUBLE NOT NULL , `lat` DOUBLE NOT NULL , `name` CHAR(40) NOT NULL , `poitype` CHAR(7) NOT NULL , `bizarea` CHAR(30) NOT NULL , `address` CHAR(100) NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;
LOAD DATA LOCAL INFILE "/datahouse/tao.jiang/baseData/mongoUTF8.csv" INTO TABLE pbaseCluster COLUMNS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '' ESCAPED BY '"' LINES TERMINATED BY '\n' (@col1,@col2,@col3,@col4,@col5,@col6,@col7,@col8) set nid=@col1,name=@col3,lat=@col7,lng=@col6,poitype=@col2,bizarea=@col4,address=@col5;

ALTER TABLE `pbaseCluster` ADD `m12_default` TINYINT NOT NULL DEFAULT '-1' AFTER `address`, ADD `d_001_10` TINYINT NOT NULL DEFAULT '-1' AFTER `m12_default`;

-- pbaseCluster cluster result importing
CREATE TEMPORARY TABLE `stvis`.`your_temp_table` ( `nid` CHAR(18) NOT NULL , `m12_default` TINYINT NOT NULL , `d_001_10` TINYINT NOT NULL ) ENGINE = InnoDB;

LOAD DATA INFILE '/datahouse/tao.jiang/clusterPOI/dbscanResult_ms3_eps_0.010000_sam_10'
INTO TABLE `your_temp_table`
FIELDS TERMINATED BY ','
(nid, m12_default, d_001_10); 

UPDATE `stvis`.`pbaseCluster` A
INNER JOIN `stvis`.`your_temp_table` B on A.nid = B.nid
SET A.m12_default = B.m12_default, A.d_001_10 = B.d_001_10;

DROP TEMPORARY TABLE `your_temp_table`;

-- tripflow construction