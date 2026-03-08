from __future__ import annotations

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "bible_art.db"
SCHEMA_PATH = BASE_DIR / "bible_art_seed.sql"


STORIES = [
    # Old Testament (20)
    {"title": "Creation", "testament": "Old", "summary": "God creates the heavens, the earth, and humanity."},
    {"title": "The Fall", "testament": "Old", "summary": "Adam and Eve disobey God in Eden and face exile."},
    {"title": "Noah and the Flood", "testament": "Old", "summary": "God judges corruption with a flood and preserves Noah's family."},
    {"title": "Tower of Babel", "testament": "Old", "summary": "Human pride at Babel leads to scattered nations and languages."},
    {"title": "Call of Abraham", "testament": "Old", "summary": "God calls Abram to leave home and promises blessing."},
    {"title": "Binding of Isaac", "testament": "Old", "summary": "Abraham's faith is tested on Mount Moriah."},
    {"title": "Jacob Wrestles", "testament": "Old", "summary": "Jacob wrestles through the night and receives a new name."},
    {"title": "Joseph in Egypt", "testament": "Old", "summary": "Joseph rises from slavery to leadership and saves many from famine."},
    {"title": "Moses and the Burning Bush", "testament": "Old", "summary": "God calls Moses to deliver Israel from Egypt."},
    {"title": "The Exodus", "testament": "Old", "summary": "Israel leaves Egypt under Moses after the plagues."},
    {"title": "Crossing the Red Sea", "testament": "Old", "summary": "God parts the sea and rescues Israel from Pharaoh's army."},
    {"title": "Giving of the Law", "testament": "Old", "summary": "At Sinai, God gives commandments and covenant law."},
    {"title": "Joshua at Jericho", "testament": "Old", "summary": "Jericho falls as Israel follows God's unusual battle plan."},
    {"title": "David and Goliath", "testament": "Old", "summary": "Young David defeats the Philistine giant Goliath."},
    {"title": "David Becomes King", "testament": "Old", "summary": "David is established as king over Israel in Jerusalem."},
    {"title": "Solomon Builds the Temple", "testament": "Old", "summary": "Solomon constructs a temple for worship in Jerusalem."},
    {"title": "Elijah at Mount Carmel", "testament": "Old", "summary": "Elijah confronts prophets of Baal and God answers by fire."},
    {"title": "Jonah and Nineveh", "testament": "Old", "summary": "Jonah preaches repentance and Nineveh turns from evil."},
    {"title": "Daniel in the Lions' Den", "testament": "Old", "summary": "Daniel remains faithful despite a decree and is delivered from lions."},
    {"title": "Return from Exile", "testament": "Old", "summary": "Exiles return from Babylon and begin rebuilding Jerusalem."},
    # New Testament (20)
    {"title": "Annunciation", "testament": "New", "summary": "Gabriel announces to Mary that she will bear Jesus."},
    {"title": "Nativity of Jesus", "testament": "New", "summary": "Jesus is born in Bethlehem and laid in a manger."},
    {"title": "Visit of the Magi", "testament": "New", "summary": "Magi from the east worship the child Jesus with gifts."},
    {"title": "Baptism of Jesus", "testament": "New", "summary": "Jesus is baptized in the Jordan and publicly affirmed."},
    {"title": "Temptation in the Wilderness", "testament": "New", "summary": "Jesus resists temptation during forty days in the wilderness."},
    {"title": "Sermon on the Mount", "testament": "New", "summary": "Jesus teaches disciples about kingdom righteousness."},
    {"title": "Calling of the Twelve", "testament": "New", "summary": "Jesus appoints twelve apostles for ministry."},
    {"title": "Feeding of the Five Thousand", "testament": "New", "summary": "Jesus multiplies loaves and fish for a great crowd."},
    {"title": "Walking on Water", "testament": "New", "summary": "Jesus walks on the sea and strengthens the disciples' faith."},
    {"title": "Transfiguration", "testament": "New", "summary": "Jesus is transfigured before selected disciples."},
    {"title": "Raising of Lazarus", "testament": "New", "summary": "Jesus raises Lazarus from the dead near Jerusalem."},
    {"title": "Triumphal Entry", "testament": "New", "summary": "Jesus enters Jerusalem as crowds welcome him."},
    {"title": "Last Supper", "testament": "New", "summary": "Jesus shares Passover with disciples and institutes communion."},
    {"title": "Crucifixion", "testament": "New", "summary": "Jesus is crucified outside Jerusalem."},
    {"title": "Resurrection", "testament": "New", "summary": "Jesus rises from the dead on the third day."},
    {"title": "Great Commission", "testament": "New", "summary": "The risen Jesus sends disciples to all nations."},
    {"title": "Pentecost", "testament": "New", "summary": "The Holy Spirit empowers believers in Jerusalem."},
    {"title": "Conversion of Paul", "testament": "New", "summary": "Saul encounters the risen Christ on the road to Damascus."},
    {"title": "Peter and Cornelius", "testament": "New", "summary": "Peter visits Cornelius and sees Gentiles receive the Spirit."},
    {"title": "Paul in Athens", "testament": "New", "summary": "Paul proclaims the gospel at the Areopagus."},
]

CHARACTERS = [
    ("Abraham", "Patriarch called by God to become father of many nations."),
    ("Isaac", "Son of Abraham and Sarah; child of promise."),
    ("Jacob", "Patriarch renamed Israel."),
    ("Joseph", "Son of Jacob who rose to power in Egypt."),
    ("Moses", "Leader of Israel in the exodus from Egypt."),
    ("Joshua", "Successor to Moses and leader into Canaan."),
    ("David", "Shepherd, king, and psalmist of Israel."),
    ("Solomon", "King known for wisdom and temple building."),
    ("Elijah", "Prophet who challenged Baal worship."),
    ("Jonah", "Prophet sent to Nineveh."),
    ("Daniel", "Exile known for faithful witness in Babylon."),
    ("Mary", "Mother of Jesus."),
    ("Jesus", "Central figure of the New Testament."),
    ("Peter", "Disciple and apostolic leader in Jerusalem."),
    ("Paul", "Apostle to the Gentiles."),
    ("John the Baptist", "Prophet who baptized Jesus."),
    ("Lazarus", "Man raised from the dead by Jesus."),
    ("Gabriel", "Angel who announced Jesus' birth."),
]

LOCATIONS = [
    ("Jerusalem", "Historic city central to many biblical events."),
    ("Bethlehem", "Birthplace of David and Jesus."),
    ("Nazareth", "Town in Galilee associated with Jesus' upbringing."),
    ("Mount Sinai", "Traditional site of covenant and law giving."),
    ("Babylon", "Major Mesopotamian city tied to exile."),
    ("Galilee", "Region where much of Jesus' ministry occurred."),
    ("Eden", "Garden where humanity's first story unfolds."),
    ("Egypt", "Land of Joseph's leadership and Israelite slavery."),
    ("Jericho", "Canaanite city captured under Joshua."),
    ("Mount Carmel", "Site of Elijah's contest with prophets of Baal."),
    ("Nineveh", "Assyrian city addressed by Jonah."),
    ("Damascus", "City near Paul's conversion encounter."),
    ("Athens", "Greek city where Paul spoke at the Areopagus."),
]

STORY_CHARACTER_LINKS = {
    "Creation": ["Abraham"],
    "The Fall": ["Abraham"],
    "Noah and the Flood": ["Abraham"],
    "Tower of Babel": ["Abraham"],
    "Call of Abraham": ["Abraham"],
    "Binding of Isaac": ["Abraham", "Isaac"],
    "Jacob Wrestles": ["Jacob"],
    "Joseph in Egypt": ["Joseph", "Jacob"],
    "Moses and the Burning Bush": ["Moses"],
    "The Exodus": ["Moses"],
    "Crossing the Red Sea": ["Moses"],
    "Giving of the Law": ["Moses"],
    "Joshua at Jericho": ["Joshua"],
    "David and Goliath": ["David"],
    "David Becomes King": ["David"],
    "Solomon Builds the Temple": ["Solomon", "David"],
    "Elijah at Mount Carmel": ["Elijah"],
    "Jonah and Nineveh": ["Jonah"],
    "Daniel in the Lions' Den": ["Daniel"],
    "Return from Exile": ["Daniel"],
    "Annunciation": ["Mary", "Gabriel", "Jesus"],
    "Nativity of Jesus": ["Mary", "Jesus"],
    "Visit of the Magi": ["Mary", "Jesus"],
    "Baptism of Jesus": ["Jesus", "John the Baptist"],
    "Temptation in the Wilderness": ["Jesus"],
    "Sermon on the Mount": ["Jesus", "Peter"],
    "Calling of the Twelve": ["Jesus", "Peter"],
    "Feeding of the Five Thousand": ["Jesus", "Peter"],
    "Walking on Water": ["Jesus", "Peter"],
    "Transfiguration": ["Jesus", "Peter"],
    "Raising of Lazarus": ["Jesus", "Lazarus"],
    "Triumphal Entry": ["Jesus", "Peter"],
    "Last Supper": ["Jesus", "Peter"],
    "Crucifixion": ["Jesus", "Mary"],
    "Resurrection": ["Jesus", "Mary"],
    "Great Commission": ["Jesus", "Peter"],
    "Pentecost": ["Peter"],
    "Conversion of Paul": ["Paul", "Jesus"],
    "Peter and Cornelius": ["Peter"],
    "Paul in Athens": ["Paul"],
}

STORY_LOCATION_LINKS = {
    "Creation": ["Eden"],
    "The Fall": ["Eden"],
    "Noah and the Flood": ["Babylon"],
    "Tower of Babel": ["Babylon"],
    "Call of Abraham": ["Babylon"],
    "Binding of Isaac": ["Jerusalem"],
    "Jacob Wrestles": ["Jerusalem"],
    "Joseph in Egypt": ["Egypt"],
    "Moses and the Burning Bush": ["Mount Sinai"],
    "The Exodus": ["Egypt", "Mount Sinai"],
    "Crossing the Red Sea": ["Egypt"],
    "Giving of the Law": ["Mount Sinai"],
    "Joshua at Jericho": ["Jericho"],
    "David and Goliath": ["Jerusalem"],
    "David Becomes King": ["Jerusalem"],
    "Solomon Builds the Temple": ["Jerusalem"],
    "Elijah at Mount Carmel": ["Mount Carmel"],
    "Jonah and Nineveh": ["Nineveh"],
    "Daniel in the Lions' Den": ["Babylon"],
    "Return from Exile": ["Jerusalem", "Babylon"],
    "Annunciation": ["Nazareth"],
    "Nativity of Jesus": ["Bethlehem"],
    "Visit of the Magi": ["Bethlehem"],
    "Baptism of Jesus": ["Galilee"],
    "Temptation in the Wilderness": ["Galilee"],
    "Sermon on the Mount": ["Galilee"],
    "Calling of the Twelve": ["Galilee"],
    "Feeding of the Five Thousand": ["Galilee"],
    "Walking on Water": ["Galilee"],
    "Transfiguration": ["Galilee"],
    "Raising of Lazarus": ["Jerusalem"],
    "Triumphal Entry": ["Jerusalem"],
    "Last Supper": ["Jerusalem"],
    "Crucifixion": ["Jerusalem"],
    "Resurrection": ["Jerusalem"],
    "Great Commission": ["Galilee"],
    "Pentecost": ["Jerusalem"],
    "Conversion of Paul": ["Damascus"],
    "Peter and Cornelius": ["Jerusalem"],
    "Paul in Athens": ["Athens"],
}

ARTWORKS = [
    {"title": "The Creation of Adam", "artist": "Michelangelo", "year": 1512, "museum": "Sistine Chapel", "description": "Fresco depicting God giving life to Adam.", "related_story": "Creation"},
    {"title": "Noah's Ark", "artist": "Edward Hicks", "year": 1846, "museum": "Philadelphia Museum of Art", "description": "Folk rendering of Noah's ark narrative.", "related_story": "Noah and the Flood"},
    {"title": "Moses Breaking the Tablets of the Law", "artist": "Rembrandt", "year": 1659, "museum": "Gemäldegalerie, Berlin", "description": "Moses descends Sinai carrying the tablets.", "related_story": "Giving of the Law"},
    {"title": "David with the Head of Goliath", "artist": "Caravaggio", "year": 1610, "museum": "Galleria Borghese", "description": "Dramatic depiction of David's victory.", "related_story": "David and Goliath"},
    {"title": "The Sacrifice of Isaac", "artist": "Caravaggio", "year": 1603, "museum": "Uffizi Gallery", "description": "Angel intervenes in Abraham's test.", "related_story": "Binding of Isaac"},
    {"title": "The Annunciation", "artist": "Fra Angelico", "year": 1440, "museum": "Convent of San Marco", "description": "Gabriel announces Christ's birth to Mary.", "related_story": "Annunciation"},
    {"title": "The Nativity with the Prophets Isaiah and Ezekiel", "artist": "Duccio", "year": 1308, "museum": "National Gallery, London", "description": "Panel painting of Christ's birth.", "related_story": "Nativity of Jesus"},
    {"title": "The Last Supper", "artist": "Leonardo da Vinci", "year": 1498, "museum": "Santa Maria delle Grazie", "description": "Iconic mural of Jesus and the disciples.", "related_story": "Last Supper"},
    {"title": "The Crucifixion", "artist": "Diego Velázquez", "year": 1632, "museum": "Museo del Prado", "description": "Baroque depiction of the crucified Christ.", "related_story": "Crucifixion"},
    {"title": "The Resurrection of Christ", "artist": "Raphael", "year": 1502, "museum": "São Paulo Museum of Art", "description": "Christ rising triumphantly from the tomb.", "related_story": "Resurrection"},
]


def populate_database() -> None:
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.executescript(schema_sql)

        conn.executemany(
            "INSERT INTO stories (title, testament, summary) VALUES (?, ?, ?)",
            [(item["title"], item["testament"], item["summary"]) for item in STORIES],
        )
        conn.executemany(
            "INSERT INTO characters (name, description) VALUES (?, ?)",
            CHARACTERS,
        )
        conn.executemany(
            "INSERT INTO locations (name, description) VALUES (?, ?)",
            LOCATIONS,
        )

        story_ids = {row[1]: row[0] for row in conn.execute("SELECT id, title FROM stories")}
        character_ids = {row[1]: row[0] for row in conn.execute("SELECT id, name FROM characters")}
        location_ids = {row[1]: row[0] for row in conn.execute("SELECT id, name FROM locations")}

        story_character_rows: list[tuple[int, int]] = []
        for story_title, names in STORY_CHARACTER_LINKS.items():
            story_id = story_ids[story_title]
            for name in names:
                story_character_rows.append((story_id, character_ids[name]))
        conn.executemany(
            "INSERT INTO story_characters (story_id, character_id) VALUES (?, ?)",
            story_character_rows,
        )

        story_location_rows: list[tuple[int, int]] = []
        for story_title, names in STORY_LOCATION_LINKS.items():
            story_id = story_ids[story_title]
            for name in names:
                story_location_rows.append((story_id, location_ids[name]))
        conn.executemany(
            "INSERT INTO story_locations (story_id, location_id) VALUES (?, ?)",
            story_location_rows,
        )

        artwork_rows = [
            (item["title"], item["artist"], item["year"], item["museum"], item["description"])
            for item in ARTWORKS
        ]
        conn.executemany(
            "INSERT INTO artworks (title, artist, year, museum, description) VALUES (?, ?, ?, ?, ?)",
            artwork_rows,
        )

        artwork_ids = {row[1]: row[0] for row in conn.execute("SELECT id, title FROM artworks")}
        story_artwork_rows = [
            (story_ids[item["related_story"]], artwork_ids[item["title"]])
            for item in ARTWORKS
        ]
        conn.executemany(
            "INSERT INTO story_artworks (story_id, artwork_id) VALUES (?, ?)",
            story_artwork_rows,
        )

        conn.commit()


if __name__ == "__main__":
    populate_database()
    print(f"Seeded database at {DB_PATH}")
