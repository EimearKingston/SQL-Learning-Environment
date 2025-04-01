-- 1 
SELECT *
FROM hotels
WHERE city = 'Cork';

-- 2 
SELECT guest_name, guest_address
FROM guests
WHERE guest_address LIKE '%Limerick%'
ORDER BY guest_name;

-- 3 
SELECT *
FROM rooms
WHERE price < 70.00 AND
   room_type = 'double'
ORDER BY price;

-- 4 
SELECT *
FROM bookings
WHERE dep_date IS  NULL;

-- 5 
SELECT COUNT(hotel_num)
FROM hotels;

-- 6 
SELECT hotel_num, COUNT(*)
FROM rooms
WHERE price < 70
GROUP BY hotel_num;

-- 7 
SELECT hotels.hotel_name, COUNT(*)
FROM hotels JOIN rooms
   ON hotels.hotel_num = rooms.hotel_num
WHERE price < 70
GROUP BY hotels.hotel_num;

-- 8 
SELECT COUNT(*)
FROM
(  SELECT DISTINCT hotels.hotel_num
   FROM
      hotels JOIN rooms
      ON hotels.hotel_num = rooms.hotel_num
   WHERE 
     rooms.price < 70.00 AND
     rooms.room_type = 'double'
) AS X;

-- 9 
SELECT AVG(price)
FROM rooms;

-- 10 
SELECT AVG(price)
FROM hotels JOIN rooms 
  ON hotels.hotel_num = rooms.hotel_num
WHERE hotels.city = 'Cork';

-- 11 
SELECT AVG(price)
FROM hotels JOIN rooms 
  ON hotels.hotel_num = rooms.hotel_num
WHERE hotels.city = 'Cork' AND
   room_type = 'double';

-- 12 
SELECT hotel_id, COUNT(*)
FROM bookings
WHERE arr_date BETWEEN '2012-11-01' AND '2012-11-31';

SELECT name, COUNT(*)
FROM hotels JOIN bookings
   ON hotels.hotel_num = bookings.hotel_num
WHERE arr_date BETWEEN '2012-11-01' AND '2012-11-31';

-- 13 
SELECT room_num, room_type, price
FROM hotels JOIN rooms
   ON hotels.hotel_num = rooms.hotel_num
WHERE hotels.hotel_name = 'Hotel Splendide';

-- 14 
SELECT
  hotels.hotel_name AS 'Hotel', 
  COUNT(*) AS 'No. Rooms'
FROM
   hotels JOIN rooms
   ON hotels.hotel_num = rooms.hotel_num
WHERE city = 'Galway'
GROUP BY hotels.hotel_num;

--15 
SELECT
  guests.guest_name AS 'Guest', 
  bookings.arr_date AS 'Arriving', 
  bookings.dep_date AS 'Departing'
FROM
   guests JOIN bookings JOIN hotels
   ON
      guests.guest_num = bookings.guest_num AND
      bookings.hotel_num = hotels.hotel_num
WHERE hotels.hotel_name = 'Hotel Splendide' AND
   bookings.arr_date BETWEEN '2013-01-01' AND '2012-01-31';
 
-- 16  
SELECT
   h1.hotel_name, h1.city, h2.city
FROM hotels AS h1 JOIN hotels AS h2
   ON h1.hotel_name = h2.hotel_name AND
      h1.hotel_num < h2.hotel_num;
	  
-- 17 
SELECT
  g.guest_name AS 'Guest',
  b.arr_date AS 'Arrived',
  b.dep_date AS 'Departing'
FROM
   guests AS g JOIN
   bookings AS b JOIN
   hotels AS h
   ON g.guest_num = b.guest_num AND
      b.hotel_num = h.hotel_num
WHERE
   CURDATE() BETWEEN b.arr_date AND b.dep_date;
   
   -- For SQLite us DATE('now') instead of CURDATE
   
-- 18 
SELECT
   g.guest_name AS 'Guest', 
   h1.hotel_name AS 'Hotel 1', h1.city AS 'In',
   h2.hotel_name AS 'Hotel 2', h2.city AS 'In'
FROM
   guests AS g JOIN
   bookings AS b1 JOIN
   hotels AS h1 JOIN
   bookings AS b2 JOIN
   hotels AS h2 
   ON g.guest_num = b1.guest_num AND
      b1.hotel_num = h1.hotel_num AND
      g.guest_num = b2.guest_num AND
      b2.hotel_num = h2.hotel_num AND
      b1.arr_date = b2.arr_date AND
      b1.dep_date = b2.dep_date AND
      h1.city < h2.city;

-- 19 	
SELECT
   g.guest_name , COUNT(*)
FROM
   guests AS g JOIN
   bookings AS b JOIN
   hotels AS h 
   ON g.guest_num = b.guest_num AND
      b.hotel_num = h.hotel_num
WHERE h.hotel_name = 'Hotel California'
GROUP BY g.guest_num
HAVING COUNT(*) > 3;

-- 20 -- Slightly devious! 
SELECT 
   (  
     SELECT COUNT(*)
      FROM
         hotels JOIN bookings
         ON hotels.hotel_num = bookings.hotel_num
      WHERE
         bookings.arr_date <= '2013-01-01' AND
         '2013-01-01' < bookings.dep_date
   ) /
   (  
      SELECT COUNT(*)
      FROM
         hotels JOIN rooms
         ON hotels.hotel_num = rooms.hotel_num
      WHERE hotels.hotel_name = 'Hotel Splendide'
   ) AS 'Occupancy %';

-- 21 
SELECT 
   g.guest_num AS 'Guest No.', 
   g.guest_name AS 'Guest Name', 
   COUNT(*) AS 'No. Bookings'
FROM
   guests AS g JOIN
   bookings AS b1
   ON g.guest_num = b1.guest_num
WHERE
   b1.arr_date BETWEEN '2002-01-01' AND '2002-12-31'
GROUP BY g.guest_num
HAVING COUNT(*) = 
(   
   SELECT MAX(num_bookings) AS 'max'
   FROM
   (  
      SELECT COUNT(*) AS 'num_bookings'
      FROM
         bookings AS b2 
      WHERE b2.arr_date BETWEEN '2002-01-01' AND '2002-12-31'
     GROUP BY b2.guest_num
   ) AS bookings_count
);

-- 22 -- similar to above
SELECT 
   h.hotel_num AS 'Hotel No.', 
   h.hotel_name AS 'Hotel Name', 
   COUNT(*) AS 'No. Bookings'
FROM
   hotels AS h JOIN
   bookings AS b1
   ON h.hotel_num = b1.hotel_num
WHERE
   b1.arr_date BETWEEN '2002-01-01' AND '2002-12-31'
GROUP BY h.hotel_num
HAVING COUNT(*) = 
(  
   SELECT MAX(num_bookings) AS 'max'
   FROM
   (  -- Return no. of bookings per hotel 
      SELECT COUNT(*) AS 'num_bookings'
      FROM
         bookings AS b2 
      WHERE b2.arr_date BETWEEN '2002-01-01' AND '2002-12-31'
     GROUP BY b2.hotel_num
   ) AS bookings_count
);

-- 23 
SELECT 
   g1.guest_name AS 'Guest 1', 
   g2.guest_name AS 'Guest 2', 
   g1.guest_address AS 'Shared Address'
FROM
   guests AS g1 JOIN
   guests AS g2
   ON g1.guest_address = g2.guest_address  AND
     g1.guest_num < g2.guest_num;
	 
-- 24 

-- 25 
SELECT MAX(staylength)
FROM
(
   SELECT arr_date, dep_date, 
      DATEDIFF(dep_date, arr_date) AS 'staylength'
   FROM bookings
   WHERE arr_date BETWEEN '2002-01-01' AND '2002-12-31'
) AS lengthofstay;

