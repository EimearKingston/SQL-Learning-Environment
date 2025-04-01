-- 1) 

SELECT COUNT(*)
FROM movies;

-- 2)
SELECT yr, COUNT(*)
FROM movies
WHERE yr = 1975
GROUP BY yr;

-- 3)
SELECT movieid
FROM actors JOIN castings
   ON id = actorid
WHERE name = 'Clint Eastwood';

-- 4)
SELECT m.title, m.yr
FROM 
   actors AS a JOIN 
   castings AS c  JOIN
   movies AS m
   ON a.id = c.actorid AND
   c.movieid = m.id
WHERE name = 'Clint Eastwood'
ORDER BY yr;

-- 5)
SELECT actorid
FROM castings
WHERE movieid =
(  SELECT id FROM movies WHERE title = 'Citizen Kane'
);
-- 6)
SELECT DISTINCT name
FROM
   actors AS a JOIN
   movies AS m JOIN
   castings AS c
   ON a.id = c.actorid AND
   m.id = c.movieid AND
   (  m.title = 'Vertigo' OR
      m.title = 'Rear Window'
   );

-- 7)
SELECT title
FROM movies
WHERE director = 28;

-- 8)
SELECT m2.title, m2.yr
FROM 
   movies AS m1 JOIN
   movies AS m2
   ON m1.director = m2.director AND
   m1.title = 'Godfather, The';

-- 9)  
SELECT * 
FROM movies
WHERE 
  title LIKE '%II' OR
  title LIKE '%III' OR
  title LIKE '%IV' OR
  title LIKE '%V' ;

-- 10)
SELECT m1.title, m1.yr, m2.title, m2.yr
FROM movies AS m1
JOIN movies AS m2
ON m2.title LIKE m1.title || '%II';


-- 11)
SELECT m1.director, m1.title, m2.title
FROM
   movies AS m1 JOIN
   movies AS m2
   ON m1.director = m2.director 
WHERE m1.score < 3 AND m2.score > 8;

-- 12)
SELECT movies.title, movies.yr
FROM 
  movies JOIN
  actors AS star1 JOIN
  castings AS is_in1 JOIN
  actors AS star2 JOIN
  castings AS is_in2
  ON star1.name = 'Clint Eastwood' AND
     star2.name = 'Richard Burton' AND
     star1.id = is_in1.actorid AND
     star2.id = is_in2.actorid AND
     is_in1.movieid = movies.id AND
     is_in2.movieid = movies.id;
     
-- 13)	 
SELECT star1.name, movies.title
FROM
   actors AS star1 JOIN
   actors AS star2 JOIN
   castings AS is_in1 JOIN
   castings AS is_in2 JOIN
   movies
   ON star2.name = 'Al Pacino' AND
   star1.name <> 'Al Pacino' AND
   is_in2.actorid = star2.id AND
   is_in1.actorid = star1.id AND
   is_in1.movieid = is_in2.movieid AND
   is_in1.movieid = movies.id;

-- 14)
SELECT a.name
FROM
   actors AS a JOIN
   movies AS m1 JOIN
   castings AS c1  JOIN
   movies AS m2 JOIN
   castings AS c2 
   ON
     a.id = c1.actorid AND
     m1.id = c1.movieid  AND
     a.id = c2.actorid AND
     m2.id = c2.movieid 
WHERE 
     m1.title = 'Casablanca' AND
     m2.title = 'Big Sleep, The';
     
  
-- 15)   
SELECT s1.name, m1.title, m1.yr, m2.title, m2.yr
FROM
   actors AS s1 JOIN
   castings AS in1 JOIN
   movies AS m1 JOIN
   actors AS s2 JOIN
   castings AS in2 JOIN
   movies AS m2
   ON s1.id = in1.actorid AND
   in1.movieid = m1.id AND
   (m1.yr BETWEEN 1950 AND 1959) AND
   s2.id = in2.actorid AND
   in2.movieid = m2.id AND
   (m2.yr BETWEEN 1980 AND 1989) AND
   s1.id = s2.id;

-- 16)   
SELECT COUNT(*), MIN(title), MAX(title)
FROM movies
WHERE yr BETWEEN 1960 AND 1969
GROUP BY yr;

-- 17)
SELECT name, COUNT(*)
FROM 
   actors JOIN castings
   ON actors.id = castings.actorid
GROUP BY name
HAVING COUNT(*) >= 10; 

SELECT  a.name, m.title
FROM actors AS a
	JOIN castings AS c1
	JOIN movies AS m
	JOIN castings AS c2
	ON a.id = c1.actorid AND a.id = c2.actorid AND c1.movieid = m.id
GROUP BY c1.actorid, c1.movieid
HAVING COUNT(c2.movieid) >= 10;


    
