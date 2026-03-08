PRAGMA foreign_keys = ON;

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
    testament TEXT NOT NULL CHECK(testament IN ('Old Testament', 'New Testament')),
    scripture_reference TEXT,
    summary TEXT,
    description TEXT
);

CREATE TABLE characters (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    testament TEXT,
    description TEXT
);

CREATE TABLE locations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    region TEXT,
    description TEXT
);

CREATE TABLE artworks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    artist TEXT,
    year INTEGER,
    medium TEXT,
    current_location TEXT,
    description TEXT,
    related_story_id INTEGER,
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

INSERT INTO stories (id, title, testament, scripture_reference, summary, description) VALUES
(1, 'Creation', 'Old Testament', 'Genesis 1-2', 'God creates the heavens and the earth in ordered days.', 'A foundational narrative describing the creation of the world, humanity, and the Sabbath rest.'),
(2, 'Noah and the Flood', 'Old Testament', 'Genesis 6-9', 'Noah obeys God and survives the flood in the ark.', 'A story of judgment, preservation, covenant, and new beginnings after the floodwaters recede.'),
(3, 'Abraham and Isaac', 'Old Testament', 'Genesis 22', 'Abraham is tested and God provides a ram.', 'A dramatic episode about faith, trust, and divine provision on Mount Moriah.'),
(4, 'Moses and the Exodus', 'Old Testament', 'Exodus 1-14', 'God delivers Israel from Egypt through Moses.', 'The central liberation narrative of the Hebrew Bible, culminating in crossing the Red Sea.'),
(5, 'David and Goliath', 'Old Testament', '1 Samuel 17', 'Young David defeats the Philistine giant.', 'A story about courage, faith, and reversal of expectations in Israel''s history.'),
(6, 'Daniel in the Lions'' Den', 'Old Testament', 'Daniel 6', 'Daniel is preserved in the lions'' den.', 'A testimony to faithfulness during exile and deliverance from imperial persecution.'),
(7, 'The Nativity of Jesus', 'New Testament', 'Luke 2; Matthew 1-2', 'Jesus is born in Bethlehem.', 'The incarnation narrative featuring Mary, Joseph, shepherds, and angelic proclamation.'),
(8, 'The Baptism of Jesus', 'New Testament', 'Matthew 3; Mark 1; Luke 3', 'Jesus is baptized by John in the Jordan.', 'A theophanic moment that marks the beginning of Jesus'' public ministry.'),
(9, 'The Good Samaritan', 'New Testament', 'Luke 10:25-37', 'A parable redefining neighbor-love.', 'Jesus teaches that mercy transcends ethnic and religious boundaries.'),
(10, 'The Last Supper', 'New Testament', 'Matthew 26; Mark 14; Luke 22; John 13', 'Jesus shares a final meal with his disciples.', 'A covenantal meal connected with service, remembrance, and impending betrayal.'),
(11, 'The Crucifixion', 'New Testament', 'Matthew 27; Mark 15; Luke 23; John 19', 'Jesus is crucified at Golgotha.', 'The passion account at the center of Christian theology and art.'),
(12, 'The Resurrection', 'New Testament', 'Matthew 28; Mark 16; Luke 24; John 20', 'Jesus rises from the dead.', 'The empty tomb and post-resurrection appearances launch the apostolic witness.');

INSERT INTO characters (id, name, testament, description) VALUES
(1, 'Adam', 'Old Testament', 'First man in Genesis creation account.'),
(2, 'Eve', 'Old Testament', 'First woman in Genesis creation account.'),
(3, 'Noah', 'Old Testament', 'Righteous man who builds the ark.'),
(4, 'Abraham', 'Old Testament', 'Patriarch called by God.'),
(5, 'Isaac', 'Old Testament', 'Son of Abraham and Sarah.'),
(6, 'Moses', 'Old Testament', 'Prophet and leader of the Exodus.'),
(7, 'David', 'Old Testament', 'Future king of Israel who defeats Goliath.'),
(8, 'Goliath', 'Old Testament', 'Philistine champion defeated by David.'),
(9, 'Daniel', 'Old Testament', 'Exiled Judean known for wisdom and faithfulness.'),
(10, 'Mary', 'New Testament', 'Mother of Jesus.'),
(11, 'Joseph', 'New Testament', 'Guardian of Jesus in infancy narratives.'),
(12, 'John the Baptist', 'New Testament', 'Prophet who baptizes Jesus.'),
(13, 'Jesus', 'New Testament', 'Central figure of the New Testament.'),
(14, 'Peter', 'New Testament', 'Disciple in the apostolic circle.'),
(15, 'Judas Iscariot', 'New Testament', 'Disciple who betrays Jesus.'),
(16, 'The Samaritan', 'New Testament', 'Merciful traveler in Jesus'' parable.');

INSERT INTO locations (id, name, region, description) VALUES
(1, 'Eden', 'Mesopotamia (traditional)', 'Garden where Adam and Eve dwell.'),
(2, 'Ararat', 'Armenian Highlands (traditional)', 'Mountains associated with the ark''s resting place.'),
(3, 'Moriah', 'Jerusalem region (traditional)', 'Mountain associated with Abraham''s test.'),
(4, 'Egypt', 'North Africa', 'Land of Israel''s slavery before the Exodus.'),
(5, 'Red Sea', 'Sinai region', 'Waters crossed during the Exodus.'),
(6, 'Valley of Elah', 'Judah', 'Battlefield of David and Goliath.'),
(7, 'Babylon', 'Mesopotamia', 'Imperial city during Judean exile.'),
(8, 'Bethlehem', 'Judea', 'Birthplace of Jesus.'),
(9, 'Jordan River', 'Levant', 'Site associated with Jesus'' baptism.'),
(10, 'Jericho Road', 'Judea', 'Road setting for the Good Samaritan parable.'),
(11, 'Jerusalem', 'Judea', 'Location of Last Supper and Passion events.'),
(12, 'Golgotha', 'Jerusalem', 'Site of the crucifixion.'),
(13, 'Empty Tomb', 'Jerusalem', 'Traditional site associated with resurrection narratives.');

INSERT INTO artworks (id, title, artist, year, medium, current_location, description, related_story_id) VALUES
(1, 'The Creation of Adam', 'Michelangelo', 1512, 'Fresco', 'Sistine Chapel, Vatican City', 'Iconic panel from the Sistine Chapel ceiling depicting God and Adam.', 1),
(2, 'Noah''s Ark', 'Edward Hicks', 1846, 'Oil on canvas', 'Philadelphia Museum of Art', 'Folk-style depiction of animals gathering at the ark.', 2),
(3, 'The Sacrifice of Isaac', 'Caravaggio', 1603, 'Oil on canvas', 'Uffizi Gallery, Florence', 'Dramatic chiaroscuro rendering of Abraham''s near-sacrifice of Isaac.', 3),
(4, 'The Crossing of the Red Sea', 'Nicolas Poussin', 1634, 'Oil on canvas', 'National Gallery of Victoria', 'Classical composition of Israel''s escape through the sea.', 4),
(5, 'David with the Head of Goliath', 'Caravaggio', 1610, 'Oil on canvas', 'Galleria Borghese, Rome', 'Psychologically intense portrayal of David after battle.', 5),
(6, 'Daniel in the Lions'' Den', 'Peter Paul Rubens', 1614, 'Oil on canvas', 'National Gallery of Art, Washington, D.C.', 'Baroque depiction of Daniel unharmed among lions.', 6),
(7, 'The Nativity', 'Geertgen tot Sint Jans', 1490, 'Oil on panel', 'National Gallery, London', 'Night scene emphasizing divine light in Christ''s birth.', 7),
(8, 'The Baptism of Christ', 'Andrea del Verrocchio and Leonardo da Vinci', 1475, 'Tempera and oil on panel', 'Uffizi Gallery, Florence', 'Renaissance treatment of Jesus'' baptism in the Jordan.', 8),
(9, 'The Good Samaritan', 'Vincent van Gogh', 1890, 'Oil on canvas', 'Kröller-Müller Museum, Otterlo', 'Expressive reinterpretation after Delacroix of the Samaritan parable.', 9),
(10, 'The Last Supper', 'Leonardo da Vinci', 1498, 'Tempera on gesso', 'Santa Maria delle Grazie, Milan', 'Monumental mural capturing Jesus'' announcement of betrayal.', 10),
(11, 'Christ Crucified', 'Diego Velázquez', 1632, 'Oil on canvas', 'Museo del Prado, Madrid', 'Meditative single-figure crucifixion image.', 11),
(12, 'The Resurrection of Christ', 'Raphael', 1502, 'Oil on panel', 'São Paulo Museum of Art', 'Triumphant portrayal of the risen Christ above sleeping guards.', 12);

INSERT INTO story_characters (story_id, character_id) VALUES
(1, 1), (1, 2),
(2, 3),
(3, 4), (3, 5),
(4, 6),
(5, 7), (5, 8),
(6, 9),
(7, 10), (7, 11), (7, 13),
(8, 12), (8, 13),
(9, 13), (9, 16),
(10, 13), (10, 14), (10, 15),
(11, 13),
(12, 13), (12, 10);

INSERT INTO story_locations (story_id, location_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4), (4, 5),
(5, 6),
(6, 7),
(7, 8),
(8, 9),
(9, 10),
(10, 11),
(11, 11), (11, 12),
(12, 11), (12, 13);

INSERT INTO story_artworks (story_id, artwork_id) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),
(7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12);
