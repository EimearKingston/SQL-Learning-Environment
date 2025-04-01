SELECT * FROM students; 
SELECT * FROM hotels; 
SELECT * FROM knows; 
SELECT * FROM likes; 
SELECT * FROM persons; 
SELECT * FROM candidates; 
SELECT * FROM countries; 
SELECT * FROM actors; 
SELECT * FROM castings; 
SELECT * FROM movies;  
SELECT actorid
FROM castings
WHERE movieid =
(  SELECT id FROM movies WHERE title = "Big Sleep, The"
);
SELECT * FROM questions; 

SELECT COUNT(*)
FROM movies; 

SELECT * 
FROM workbooks; 

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


