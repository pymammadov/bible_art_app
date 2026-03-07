CREATE TABLE stories (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    testament TEXT,
    description TEXT
);

CREATE TABLE characters (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE locations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE artworks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    artist TEXT,
    year INTEGER,
    description TEXT
);

CREATE TABLE story_characters (
    story_id INTEGER,
    character_id INTEGER
);

CREATE TABLE story_locations (
    story_id INTEGER,
    location_id INTEGER
);

CREATE TABLE story_artworks (
    story_id INTEGER,
    artwork_id INTEGER
);
