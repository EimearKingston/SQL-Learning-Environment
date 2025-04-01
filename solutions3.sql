/* 1 */
SELECT MAX(population)
FROM countries;

/* 2 */
SELECT MAX(population)
FROM countries
WHERE region = 'Africa';

/* 3 */
SELECT SUM(gdp)
FROM countries
WHERE region = 'Europe';


-- 4
SELECT population
FROM countries
WHERE gdp is NULL;

-- 5
SELECT population
FROM countries
WHERE gdp is not NULL;


-- 6
SELECT region, AVG(gdp)
FROM countries
GROUP BY region;

-- 7
-- Note Sqlite uses || for string concatenation.
SELECT * 
FROM countries
-- WHERE name LIKE CONCAT('%', region, '%');
WHERE name LIKE '%' || region || '%';

-- 8
SELECT region, MIN(gdp/population), MAX(gdp/population)
FROM countries
GROUP BY region;

-- 9 
SELECT region, COUNT(*), SUM(population)
FROM countries
WHERE region IN ('Europe', 'Middle East', 'Africa')
GROUP BY region;

-- 10
SELECT  SUM(population), SUM(area), SUM(gdp)
FROM countries
WHERE name IN ('France', 'Germany', 'Spain');

-- 11
/* Excludes regions with no qualifying
countries */
SELECT  region, COUNT(*)
FROM countries
WHERE population > 100000000
GROUP BY region;

-- 12
-- SQLite SUBSTRING(X, Y, Z) yields substring of X
-- the starts in position Y (starting from 1) and 
-- is Z characters long.
SELECT SUBSTRING(name, 1, 1), COUNT(*), MIN(name), MAX(name)
FROM countries
GROUP BY SUBSTRING(name, 1, 1);

-- 13
SELECT  region, name, population
FROM countries
ORDER BY region, population DESC;

-- 14
SELECT region, COUNT(*), SUM(area)/SUM(population)
FROM countries
GROUP BY region
HAVING SUM(population) > 1000000000;

-- ===========================================
-- Queries below rely of joins etc and can be
-- tackled later once we have cover those concepts.

-- 15
SELECT c2.region, c2.name
FROM 
  countries AS c1 JOIN
  countries AS c2
  ON c1.region = c2.region
WHERE c1.name = 'Jordan';

-- 16
SELECT COUNT(*)
FROM 
  countries AS c1 JOIN
  countries AS c2
  ON c1.region = c2.region
WHERE c1.name = 'Jordan';

-- 17
SELECT c2.name
FROM 
  countries AS c1 JOIN
  countries AS c2
  ON c1.region = c2.region 
WHERE c1.name = 'Spain' AND
  c2.area > c1.area;

-- 18
SELECT c1.name, c1.area, 
   SUM(c2.area) AS 'region area',
   c1.area*100/SUM(c2.area) AS '%'
FROM 
  countries AS c1 CROSS JOIN
  countries AS c2
GROUP BY c1.name
HAVING c1.area > 0.05*SUM(c2.area);



-- 19
/* Vatican is listed with NULL population */
SELECT TRUNCATE(population/100000000, 0), COUNT(*)
FROM countries
WHERE NOT population  IS NULL
GROUP BY TRUNCATE(population/100000000, 0);

-- 20
SELECT MIN(c2.population)
FROM 
  countries AS c1 JOIN
  countries AS c2
  ON c1.region = c2.region AND
  c1.name = 'China';

-- 21
SELECT c2.name, c2.gdp/c2.population
FROM 
  countries AS c1 JOIN
  countries AS c2
  ON c1.name = 'China'
WHERE c1.gdp/c1.population <= c2.gdp/c2.population
ORDER BY c2.gdp/c2.population DESC;


/* 22 */
SELECT c1.name, COUNT(*)
FROM
   countries AS c1 JOIN
   countries AS c2
   ON c1.population <= c2.population
GROUP BY c1.name
HAVING COUNT(*) = 1;

SELECT ROUND(CAST(gdp AS FLOAT)
   /CAST(population AS FLOAT), 0)
FROm countries
WHERE region = 'Europe';