-- 1 количество исполнителей в каждом жанре;

SELECT title, count(artist_id) cnt FROM genre g
LEFT JOIN artist_genre ag ON g.id = ag.genre_id
GROUP BY title
ORDER BY cnt DESC 


-- 2 количество треков, вошедших в альбомы 2018-2020 годов; // под текущую базу года чуть изменил

SELECT count(*) FROM album a 
LEFT JOIN track t ON a.id  = t.album_id
WHERE a.release_year BETWEEN 2018 AND 2020

-- 3 средняя продолжительность треков по каждому альбому;

SELECT a.title, avg(duration) FROM track t 
LEFT JOIN album a ON t.album_id  = a.id 
GROUP BY a.title 

-- 4 все исполнители, которые не выпустили альбомы в 2020 году;

SELECT a.title FROM artist a  /* Получаем имена исполнителей */
WHERE a.title  NOT IN (
	SELECT a2.title  FROM artist a2 
	JOIN artist_album aa ON a2.id = aa.artist_id 
	JOIN album al ON aa.album_id = al.id  
	WHERE al.release_year = 2020
	)

-- 5 названия сборников, в которых присутствует конкретный исполнитель (выберите сами);

SELECT DISTINCT c.title, ar.title  FROM collections c 
JOIN track_collections tc ON c.id =tc.collection_id 
JOIN track t ON tc.track_id = t.id 
JOIN album al ON t.album_id = al.id 
JOIN artist_album aa ON al.id = aa.album_id 
JOIN artist ar ON aa.artist_id = ar.id 
WHERE ar.title = 'Наив'

-- 6 название альбомов, в которых присутствуют исполнители более 1 жанра;

SELECT title FROM (
	SELECT al.title, ag.artist_id , count(ag.genre_id) cnt FROM album al 
	JOIN artist_album aa ON al.id = aa.album_id 
	JOIN artist ar ON aa.artist_id = ar.id 
	JOIN artist_genre ag ON ar.id = ag.artist_id
	GROUP BY al.title, ag.artist_id ) AS t1
WHERE t1.cnt > 1

-- без вложенного запроса

SELECT al.title, count(ag.genre_id)  FROM album al 
JOIN artist_album aa ON al.id =aa.album_id 
JOIN artist ar ON aa.artist_id = ar.id
JOIN artist_genre ag ON ar.id = ag.artist_id 
GROUP BY al.title 
HAVING count(ag.genre_id) > 1

-- 7 наименование треков, которые не входят в сборники;

SELECT t.title FROM track t 
LEFT JOIN track_collections tc ON t.id = tc.track_id
WHERE tc.collection_id IS null

-- 8 исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько);

SELECT ar.title artist, t.title track, t.duration FROM artist ar 
JOIN artist_album aa ON ar.id = aa.artist_id 
JOIN album al ON aa.album_id = al.id 
JOIN track t ON al.id = t.album_id 
WHERE t.duration = (SELECT min(duration) FROM track)

-- 9 название альбомов, содержащих наименьшее количество треков.
				
SELECT al.title FROM album al
JOIN track t ON al.id = t.album_id
GROUP BY al.title 
HAVING count(t.title) = (
	SELECT count(a.title) cnt FROM album a
	JOIN track t2 ON a.id = t2.album_id
	GROUP BY a.title 
	ORDER BY cnt
	LIMIT 1
		)
				