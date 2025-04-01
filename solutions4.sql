-- 1)
SELECT * 
FROM persons JOIN likes;



-- 2)
SELECT * 
FROM persons JOIN likes
ON persons.person_id = likes.person_id;

SELECT * 
FROM persons AS p
  JOIN likes as f
ON p.person_id = f.person_id;

-- 3)
SELECT f.food
FROM persons AS p
  JOIN likes as f
  ON p.person_id = f.person_id
WHERE p.first_name = 'Aoife' AND p.last_name = 'Ahern';

-- 4)
SELECT p.first_name || ' ' || p.last_name AS 'Name', 
'likes',  f.food
FROM persons AS p
  JOIN likes as f
  ON p.person_id = f.person_id
WHERE p.county = 'Cork';

-- 5)
SELECT DISTINCT f.food
FROM persons AS p
  JOIN likes as f
  ON p.person_id = f.person_id
WHERE p.gender = 'F';


-- 6)
SELECT p.first_name, p.last_name 
FROM persons AS p
  JOIN likes as f
  ON p.person_id = f.person_id
WHERE f.food = 'Pizza';

-- 7)
SELECT DISTINCT p.town
FROM persons AS p
  JOIN likes as f
  ON p.person_id = f.person_id
WHERE f.food = 'Beer';

-- 8)

SELECT *
FROM likes as f1
  JOIN likes as f2;
  
-- 9)
SELECT *
FROM likes as f1
  JOIN likes as f2
  ON f1.person_id = f2.person_id
WHERE f1.food < f2.food;

-- 10)
SELECT f1.person_id
FROM
  likes as f1
  JOIN likes as f2
  ON f1.person_id = f2.person_id
WHERE f1.food = 'Pizza'
  AND f2.food = 'Nutella';
  

-- 11) 
SELECT person_id
FROM likes
WHERE food = 'Pizza'
  OR food = 'Nutella';
  
-- 12)
SELECT p.first_name, p.last_name 
FROM persons AS p
  JOIN likes as f
  ON p.person_id = f.person_id
WHERE 
  p.town = 'Cork'
  AND f.food = 'Beer';

-- 13) 
SELECT p.first_name, p.last_name 
FROM persons AS p
  JOIN likes as f1
  JOIN likes as f2
  ON p.person_id = f1.person_id
    AND p.person_id = f2.person_id
WHERE 
  f1.food = 'Pizza'
  AND f2.food = 'Nutella';
  
-- 14)
SELECT first_name, last_name 
FROM persons AS p
  JOIN likes as f
  ON p.person_id = f.person_id
WHERE 
  food = 'Pizza'
  OR food = 'Nutella';
  
-- 15)
SELECT *
FROM persons AS p1 JOIN persons AS p2;



-- 16)
SELECT 
   p1.first_name || ' ' || p1.last_name AS 'Name 1', 
   p2.first_name || ' ' || p2.last_name AS 'Name 2' 
FROM persons AS p1 JOIN persons AS p2
WHERE p1.person_id < p2.person_id;


-- 17)
SELECT 
   p1.first_name || ' ' || p1.last_name AS 'Name 1', 
   p2.first_name || ' ' || p2.last_name AS 'Name 2' 
FROM persons AS p1 JOIN persons AS p2
WHERE 
   p1.person_id < p2.person_id
   AND p1.birth_date = p2.birth_date;

  

-- 18)
SELECT 
   p1.first_name || ' ' || p1.last_name AS 'Name 1', 
   p2.first_name || ' ' || p2.last_name AS 'Name 2' 
FROM persons AS p1 JOIN persons AS p2
WHERE 
   p1.person_id < p2.person_id
   AND 
   
   SUBSTR(p1.birth_date, 6) = SUBSTR(p2.birth_date, 6);
   

-- 19)
SELECT food, COUNT(*) AS 'No. of fans'
FROM likes
GROUP BY food;

-- 20)

SELECT p.person_id, p.first_name, p.last_name
FROM
   persons AS p
   JOIN likes AS f1
   JOIN likes AS f2
   ON p.person_id = f1.person_id
      AND p.person_id = f2.person_id
WHERE f1.food <> 'Beer'
GROUP BY p.person_id
HAVING COUNT(DISTINCT f1.food) = COUNT(DISTINCT f2.food);



-- 21)

SELECT p.person_id, p.first_name, p.last_name
FROM
   persons AS p
   JOIN likes AS f1
   ON p.person_id = f1.person_id
WHERE f1.food IN ('Pizza', 'Beer', 'Nutella')
GROUP BY p.person_id
HAVING COUNT(f1.food) >= 2;

-- 22)

SELECT p1.first_name, p1.last_name, 'and', p2.first_name, 
p2.last_name, 'both like', f1.food 
FROM
   persons AS p1
   JOIN likes AS f1
   JOIN persons AS p2
   JOIN likes AS f2
   ON 
     p1.person_id = f1.person_id
     AND p2.person_id = f2.person_id
     AND f1.food = f2.food
WHERE
   p1.person_id < p2.person_id;

-- 23)

SELECT county, food, COUNT(*) AS 'Num'
FROM
   persons AS p
   JOIN likes AS f
   ON p.person_id = f.person_id
GROUP BY county, food;

-- 24)

SELECT county, COUNT(*)
FROM
   persons AS p
   JOIN likes AS f
   ON p.person_id = f.person_id
WHERE food = 'Beer'
GROUP BY county
ORDER BY COUNT(*) DESC;


-- 25)

SELECT p1.first_name, p1.last_name, p1.birth_date
FROM
   persons AS p1
   JOIN persons AS p2
WHERE p1.birth_date >= p2.birth_date
GROUP BY p1.person_id
HAVING COUNT(*) = 1;
