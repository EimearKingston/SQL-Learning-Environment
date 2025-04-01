-- 1) 
SELECT actorid
FROM castings
WHERE movieid =
(  SELECT id FROM movies WHERE title = "Big Sleep, The"
);

--2)
SELECT yr, title
FROM movies 
WHERE director = 
(  SELECT director
     FROM movies 
     WHERE title = 'Citizen Kane'
)
ORDER BY yr;

-- 3) 
SELECT name 
FROM actors
WHERE id IN 
( SELECT actorid
  FROM castings
  WHERE movieid =
  (  SELECT id FROM movies 
     WHERE title = "Big Sleep, The"
  )
);

-- 4)
(  SELECT id
   FROM movies
   WHERE yr BETWEEN 1950 AND 1959
)
UNION
(  SELECT movieid
   FROM castings
   WHERE actorid =
   (  SELECT id
      FROM actors
      WHERE name = "Elizabeth Taylor"
   )
);

-- 5) 
SELECT title, score
FROM movies
WHERE score = 
( SELECT MAX(score)
      FROM movies
);

-- 6)
SELECT name 
FROM actors
WHERE id IN
(  SELECT actorid
   FROM castings
   GROUP BY actorid
   HAVING COUNT(*) >= 10
);

-- 7)
SELECT title, score
FROM movies
WHERE score > 0.9*
( SELECT MAX(score)
      FROM movies
);

-- 8)
SELECT name
FROM actors
WHERE id IN
( SELECT DISTINCT actorid
  FROM castings
  WHERE movieid  IN
  ( SELECT id
    FROM movies
    WHERE score < 3.0
  )
);

-- 9)
(
  SELECT title, score
  FROM movies
  WHERE score = 
  ( SELECT MAX(score)
    FROM movies
  )
)
UNION
(
  SELECT title, score
  FROM movies
  WHERE score = 
  ( SELECT MIN(score)
    FROM movies
  )
);

-- 10)
SELECT yr, title
FROM movies
WHERE yr < ALL
( SELECT yr
  FROM movies
  WHERE director = 
  ( SELECT director
    FROM movies
    WHERE title = 'Citizen Kane'
  )
);

SELECT yr, title
FROM movies
WHERE yr > ANY
( SELECT yr
  FROM movies
  WHERE director = 
  ( SELECT director
    FROM movies
    WHERE title = 'Citizen Kane'
  )
);

-- 11)
SELECT title, score
FROM movies 
WHERE score >= ALL
(  SELECT MAX(score)
   FROM movies
   WHERE yr BETWEEN 1940 and 1949
);

-- 12)
SELECT MAX(film_count)
FROM
( SELECT director, COUNT(*) AS 'film_count'
  FROM movies
  GROUP by director
 ) AS film_counts;
 
 -- 13) 
SELECT  director, COUNT(*)
FROM movies
GROUP BY director
HAVING COUNT(*) = 
( SELECT MAX(film_count)
  FROM 
  ( SELECT director, COUNT(*) AS 'film_count'
    FROM movies
    GROUP by director
  ) AS whatever
);

-- 14) 
SELECT yr, title
FROM movies
WHERE director =
( SELECT  director
  FROM movies
  GROUP BY director
  HAVING COUNT(*) = 
  ( SELECT MAX(film_count)
    FROM 
    ( SELECT director, COUNT(*) AS 'film_count'
      FROM movies
      GROUP by director
    ) AS whatever
  )
)
ORDER BY yr;

 -- 15) 
 SELECT title 
FROM movies
WHERE id IN
( -- ids of films with DK directed by WA 
  SELECT movieid 
  FROM castings
  WHERE
    actorid =
    (  -- DK's actor id 
       SELECT id
       FROM actors
       WHERE name = 'Diane Keaton'
    ) AND
    movieid IN  
    ( -- id of WA's films 
      SELECT id 
      FROM movies
      WHERE director =
      (  SELECT director 
         FROM movies
         WHERE title = 'Bananas'
      )
    )
);




