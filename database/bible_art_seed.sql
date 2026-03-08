DROP TABLE IF EXISTS story_artworks;
DROP TABLE IF EXISTS story_locations;
DROP TABLE IF EXISTS story_characters;
DROP TABLE IF EXISTS artworks;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS characters;
DROP TABLE IF EXISTS stories;

CREATE TABLE stories (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    testament TEXT NOT NULL,
    summary TEXT NOT NULL
);

CREATE TABLE characters (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE locations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE artworks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    artist TEXT,
    year INTEGER,
    museum TEXT,
    related_story_id INTEGER,
    description TEXT,
    FOREIGN KEY (related_story_id) REFERENCES stories(id)
);

CREATE TABLE story_characters (
    story_id INTEGER NOT NULL,
    character_id INTEGER NOT NULL,
    PRIMARY KEY (story_id, character_id),
    FOREIGN KEY (story_id) REFERENCES stories(id),
    FOREIGN KEY (character_id) REFERENCES characters(id)
);

CREATE TABLE story_locations (
    story_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    PRIMARY KEY (story_id, location_id),
    FOREIGN KEY (story_id) REFERENCES stories(id),
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

CREATE TABLE story_artworks (
    story_id INTEGER NOT NULL,
    artwork_id INTEGER NOT NULL,
    PRIMARY KEY (story_id, artwork_id),
    FOREIGN KEY (story_id) REFERENCES stories(id),
    FOREIGN KEY (artwork_id) REFERENCES artworks(id)
);
