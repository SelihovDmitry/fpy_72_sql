-- создание БД музыкального сервиса

CREATE TABLE IF NOT EXISTS Album (
	id SERIAL PRIMARY KEY,
	title VARCHAR(100) NOT NULL,
	release_year INT2 CHECK(release_year > 1899 AND release_year < 2100)
	);

CREATE TABLE IF NOT EXISTS Track (
	id SERIAL PRIMARY KEY,
	title VARCHAR(50) NOT NULL,
	duration INT NOT NULL,
	album_id INT REFERENCES Album(id)
	); 

CREATE TABLE IF NOT EXISTS Artist (
	id SERIAL PRIMARY KEY,
	title VARCHAR(50) NOT NULL
	)
	
CREATE TABLE IF NOT EXISTS Genre (
	id SERIAL PRIMARY KEY,
	title VARCHAR(50) NOT NULL
	)
	
CREATE TABLE IF NOT EXISTS Artist_Genre (
	artist_id INTEGER REFERENCES Artist(id),
	genre_id INTEGER REFERENCES Genre(id),
	CONSTRAINT pk_artist_genre PRIMARY KEY (artist_id, genre_id)
	)
		
CREATE TABLE IF NOT EXISTS Artist_Album (
	artist_id INTEGER REFERENCES Artist(id),
	album_id INTEGER REFERENCES Album(id),
	CONSTRAINT pk_artist_album PRIMARY KEY (artist_id, album_id)
	)
	
CREATE TABLE Collections (
	id SERIAL PRIMARY KEY,
	title VARCHAR(100) NOT NULL,
	release_year INT2 CHECK(release_year > 1899 AND release_year < 2100)
	);
	
CREATE TABLE IF NOT EXISTS Track_Collections (
	track_id INTEGER REFERENCES Track(id),
	collection_id INTEGER REFERENCES Collections(id),
	CONSTRAINT pk_track_collections PRIMARY KEY (track_id, collection_id)
	)






