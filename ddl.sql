-- mysql
CREATE TABLE website (
	website_name VARCHAR(50) PRIMARY KEY,
	url VARCHAR(2048),
	location VARCHAR(50),
	priority INT NOT NULL
);

CREATE TABLE room (
	website_name VARCHAR(50),
	room_number VARCHAR(50),
	room_url VARCHAR(256),
	room_type VARCHAR(50) NOT NULL,
	room_price VARCHAR(50) NOT NULL,
	move_in_date VARCHAR(50) NOT NULL,
	fetch_date DATETIME NOT NULL,
	PRIMARY KEY(website_name, room_number),
	FOREIGN KEY (website_name) REFERENCES website(website_name) ON DELETE CASCADE
);

CREATE OR REPLACE VIEW v_website_room AS (
	SELECT r.*, w.url, w.location, w.priority FROM room r
	NATURAL JOIN website w
);

CREATE TABLE room_history (
	website_name VARCHAR(50) NOT NULL,
	room_number VARCHAR(50),
	room_type VARCHAR(50) NOT NULL,
	room_price VARCHAR(50) NOT NULL,
	move_in_date VARCHAR(50) NOT NULL,
	fetch_date DATETIME NOT NULL,
	PRIMARY KEY(website_name, room_number, fetch_date),
	FOREIGN KEY (website_name) REFERENCES website(website_name) ON DELETE CASCADE
);

CREATE OR REPLACE VIEW v_website_room_history AS (
	SELECT r.*, w.url, w.location, w.priority FROM room_history r
	NATURAL JOIN website w
);

CREATE TABLE fetch_status (
	website_name VARCHAR(50) NOT NULL,
	room_count INT NOT NULL,
	fetch_date DATETIME NOT NULL,
	PRIMARY KEY(website_name, fetch_date),
	FOREIGN KEY (website_name) REFERENCES website(website_name) ON DELETE CASCADE
);

CREATE OR REPLACE VIEW v_fetch_status AS (
	SELECT r.*, w.priority FROM fetch_status r
	NATURAL JOIN website w
);

CREATE TABLE sublease (
	website_name VARCHAR(50),
	room_url VARCHAR(100) NOT NULL,
	room_title VARCHAR(100) NOT NULL,
	post_date DATETIME NOT NULL,
	room_type VARCHAR(50) NOT NULL,
	room_price VARCHAR(50) NOT NULL,
	move_in_date VARCHAR(50) NOT NULL,
	fetch_date DATETIME NOT NULL,
	FOREIGN KEY (website_name) REFERENCES website(website_name) ON DELETE CASCADE
);

CREATE OR REPLACE VIEW v_website_sublease AS (
	SELECT r.*, w.url, w.location, w.priority FROM sublease r
	NATURAL JOIN website w
);
