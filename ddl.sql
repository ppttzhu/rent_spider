-- mysql
CREATE TABLE website (
	website_name VARCHAR(50) PRIMARY KEY,
	url VARCHAR(100),
	priority INT NOT NULL
);

CREATE TABLE room (
	website_name VARCHAR(50),
	room_number VARCHAR(50),
	room_type VARCHAR(50) NOT NULL,
	room_price VARCHAR(50) NOT NULL,
	move_in_date VARCHAR(500) NOT NULL,
	fetch_date DATETIME NOT NULL,
	PRIMARY KEY(website_name, room_number),
	FOREIGN KEY (website_name) REFERENCES website(website_name) ON DELETE CASCADE
);

CREATE OR REPLACE VIEW v_website_room AS (
	SELECT r.*, w.url, w.priority FROM room r
	NATURAL JOIN website w
);