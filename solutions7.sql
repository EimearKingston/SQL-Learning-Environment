/* Schema 

cities(ID, Name, CountryCode, District, Population)
countries (Code, Name, Continent, Region, SurfaceArea, IndepYear, Population,
  LifeExpectancy, GNP, GNPOld, LocalName,  GovernmentForm, HeadOfState, Capital, Code2)
 countrylanguage(CountryCode, Language, IsOfficial, Percentage)
 
 */

--  .schema countries
 
 

-- Q0
-- Review the questions on the recent test.

-- Q1
-- List the twenty most populous citiesz in the world. (MySQL's LIMIT
-- feature may prove handy here.)
SELECT name
FROM cities
ORDER BY population DESC
LIMIT 20;

-- Q2
-- List the countries that have at least five cities with a population of a one million
-- or more. List teh country's name and the number of such cities. 
SELECT code, countries.name,  COUNT(*)
FROM cities JOIN countries
   ON cities.country_code = countries.code
WHERE cities.population >= 1000000
GROUP BY countries.code
HAVING COUNT(*) >= 5
ORDER BY COUNT(*) DESC;

-- Q3
-- List all the countries which achieve independent since India
SELECT name, indep_year
FROM countries
WHERE indep_year >= 
(  SELECT indep_year 
   FROM countries
   WHERE name = 'India'
)
ORDER BY indep_year;

-- Q4
-- List those language that are spoken by a significanr proportion of the population
-- of at least six countries. We interpret "significant" to mean ``at least 25\%''.
SELECT country_languages.language, COUNT(*)
FROM countries JOIN country_languages
   ON countries.code = country_languages.country_code
WHERE percentage >= 25
GROUP BY country_languages.language
HAVING COUNT(*) >= 6;


-- Q5
-- List the names of all countries that are both among the twenty poorest (lowest
-- GNP per capita) and among the twenty with the lowest life expectancy.
-- Note: take care to filter out countries whose lefexpectancy, population or
-- GNP is unknown.
/* SELECT code,  name, gnp, population, gnp/population, life_expectancy
FROM countries 
WHERE code IN 
(  SELECT code
   FROM
   (
        SELECT code
         FROM country
         WHERE life_expectancy IS NOT NULL
         ORDER BY life_expectancy 
         LIMIT 20
      INTERSECT
        SELECT code
         FROM country
         WHERE gnp IS NOT NULL AND population IS NOT NULL
            AND population > 0
         ORDER BY GNP/population
         LIMIT 20
      
   ) AS poor_countries
   GROUP BY code
   HAVING COUNT(*) > 1
); */

SELECT code, name, life_expectancy, gnp
FROM countries
WHERE code in 
      (
      SELECT code
      FROM countries
      WHERE life_expectancy IS NOT NULL
      ORDER BY life_expectancy 
      LIMIT 20
      )
   AND
   code in 
      (
      SELECT code
      FROM countries
      WHERE gnp IS NOT NULL AND population IS NOT NULL
         AND population > 0
      ORDER BY GNP/population
      LIMIT 20
      );


-- Q6 
-- List all the countries that comrpise a "signifivcant" portion (at least 10% ) of the total
-- surface area of the continent to which they belong. As a warm up, first do this for a 
-- specific continent (say South America). You may find the notion of a correlated subquery
-- useful here (look it up).
SELECT name, surface_area
FROM countries AS c1
WHERE surface_area >= 0.1*
(  SELECT SUM(surface_area)
   FROM countries AS c2
   WHERE c1.continent = c2.continent
);


-- Q7
--  Calculate what proportion of the world's total GNP is belongs to the 20 richest (by GNP) 
-- countries
SELECT 
(  -- Total GNP of 20 richest
   SELECT SUM(gnp)
   FROM
   ( -- GNP's of world's 20 richest countries
     SELECT gnp
     FROM countries
     ORDER BY gnp DESC
     LIMIT 20
   ) AS richest20
)/
( -- Global GNP
  SELECT SUM(gnp)
  FROM countries
) AS "Prop. of 20 Richest";

-- Q8
--  Determine the head of state with the greatest amount of territory (by surface area).
SELECT name, area
FROM
(  -- list of HoSs and area under their headship
   SELECT head_of_state AS 'name', SUM(surface_area) AS 'area'
   FROM countries
   GROUP BY head_of_state
) AS area_summary1
WHERE area =
(
   SELECT MAX(area)
   FROM
   (  -- list of HoSs and area under their headship
      SELECT head_of_state AS 'name', SUM(surface_area) AS 'area'
      FROM countries
      GROUP BY head_of_state
   ) AS area_summary2
);


-- Q9
-- List for each continent, the name of the countries with the greatest and smallest population.
SELECT c1.continent, c1.name, c1.population, c2.name, c2.population, summary.smallest
FROM
   countries AS c1
   JOIN countries AS c2
   JOIN 
   (
      SELECT continent, MIN(population)  AS 'smallest', MAX(population) AS 'largest'
      FROM countries 
      GROUP BY continent
   ) AS summary
   ON c1.continent = c2.continent 
      AND c1.continent = summary.continent
WHERE c1.population = summary.largest
   AND c2.population = summary.smallest
GROUP BY c1.continent;

-- Q10
-- For each countries in Europe list the proportion of its population
-- that live in its most populous cities
SELECT countries.name AS "country", countries.population AS "totalpop", 
   c1.name AS "cities", c1.population AS "citiespop",
   c1.population * 100 / countries.population  AS "percentage"
FROM countries join cities AS c1
WHERE countries.code = c1.country_code
AND countries.continent = 'Europe'
AND c1.population = 
(  SELECT MAX(c2.population)
   FROM cities AS c2
   WHERE c2.country_code = countries.code
);

-- Q11
-- List in descending order of population all countries in which none of
-- the following languages are spoken by a significant proportion of the
-- population: English, Spanish, Chinese, Arabic or Hindi
SELECT name, population
FROM countries
WHERE code NOT IN
(  SELECT country_code
   FROM country_languages
   WHERE
      ((language = 'English') AND (percentage >= 20))
      OR ((language = 'Spanish') AND (percentage >= 20))
      OR ((language = 'Chinese') AND (percentage >= 20))
      OR ((language = 'Arabic') AND (percentage >= 20))
      OR ((language = 'Hindi') AND (percentage >= 20))
)
ORDER BY population DESC;

-- Q12
-- List all the languages that are spoken by a majority of people
-- in countries in at least two continents.
SELECT country_languages.language AS "Language",  
   COUNT(DISTINCT countries.continent) AS "Num Continents",
   COUNT(countries.name) AS "Num Countries"
FROM countries JOIN country_languages
   ON countries.code = country_languages.country_code
WHERE percentage > 50
GROUP BY country_languages.language
HAVING COUNT(DISTINCT countries.continent) > 1
ORDER BY COUNT(DISTINCT countries.continent) DESC, COUNT(countries.name) DESC

