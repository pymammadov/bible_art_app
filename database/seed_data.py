from __future__ import annotations

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "bible_art.db"
SCHEMA_PATH = BASE_DIR / "bible_art_seed.sql"


STORY_SEEDS = [
    # Old Testament
    {"title": "Creation", "testament": "Old", "summary": "God creates the heavens, the earth, and humanity.", "characters": ["God", "Adam", "Eve"], "locations": ["Eden"]},
    {"title": "The Fall", "testament": "Old", "summary": "Adam and Eve disobey God in Eden and face exile.", "characters": ["Adam", "Eve"], "locations": ["Eden"]},
    {"title": "Noah and the Flood", "testament": "Old", "summary": "God judges corruption with a flood and preserves Noah's family.", "characters": ["Noah"], "locations": ["Ararat"]},
    {"title": "Tower of Babel", "testament": "Old", "summary": "Human pride at Babel leads to scattered nations and languages.", "characters": ["Nimrod"], "locations": ["Babylon"]},
    {"title": "Call of Abraham", "testament": "Old", "summary": "God calls Abram to leave home and promises blessing.", "characters": ["Abraham"], "locations": ["Hebron"]},
    {"title": "Binding of Isaac", "testament": "Old", "summary": "Abraham's faith is tested on Mount Moriah.", "characters": ["Abraham", "Isaac"], "locations": ["Jerusalem"]},
    {"title": "Jacob Wrestles", "testament": "Old", "summary": "Jacob wrestles through the night and receives a new name.", "characters": ["Jacob"], "locations": ["Penuel"]},
    {"title": "Joseph in Egypt", "testament": "Old", "summary": "Joseph rises from slavery to leadership and saves many from famine.", "characters": ["Joseph", "Jacob"], "locations": ["Egypt"]},
    {"title": "Moses and the Burning Bush", "testament": "Old", "summary": "God calls Moses to deliver Israel from Egypt.", "characters": ["Moses"], "locations": ["Mount Sinai"]},
    {"title": "The Exodus", "testament": "Old", "summary": "Israel leaves Egypt under Moses after the plagues.", "characters": ["Moses", "Pharaoh"], "locations": ["Egypt"]},
    {"title": "Crossing the Red Sea", "testament": "Old", "summary": "God parts the sea and rescues Israel from Pharaoh's army.", "characters": ["Moses", "Pharaoh"], "locations": ["Red Sea"]},
    {"title": "Giving of the Law", "testament": "Old", "summary": "At Sinai, God gives commandments and covenant law.", "characters": ["Moses"], "locations": ["Mount Sinai"]},
    {"title": "Joshua at Jericho", "testament": "Old", "summary": "Jericho falls as Israel follows God's unusual battle plan.", "characters": ["Joshua"], "locations": ["Jericho"]},
    {"title": "David and Goliath", "testament": "Old", "summary": "Young David defeats the Philistine giant Goliath.", "characters": ["David", "Goliath"], "locations": ["Jerusalem"]},
    {"title": "David Becomes King", "testament": "Old", "summary": "David is established as king over Israel in Jerusalem.", "characters": ["David"], "locations": ["Jerusalem"]},
    {"title": "Solomon Builds the Temple", "testament": "Old", "summary": "Solomon constructs a temple for worship in Jerusalem.", "characters": ["Solomon"], "locations": ["Jerusalem"]},
    {"title": "Elijah at Mount Carmel", "testament": "Old", "summary": "Elijah confronts prophets of Baal and God answers by fire.", "characters": ["Elijah"], "locations": ["Mount Carmel"]},
    {"title": "Jonah and Nineveh", "testament": "Old", "summary": "Jonah preaches repentance and Nineveh turns from evil.", "characters": ["Jonah"], "locations": ["Nineveh"]},
    {"title": "Daniel in the Lions' Den", "testament": "Old", "summary": "Daniel remains faithful despite a decree and is delivered from lions.", "characters": ["Daniel"], "locations": ["Babylon"]},
    {"title": "Return from Exile", "testament": "Old", "summary": "Exiles return from Babylon and begin rebuilding Jerusalem.", "characters": ["Ezra", "Nehemiah"], "locations": ["Jerusalem", "Babylon"]},
    # New Testament
    {"title": "Annunciation", "testament": "New", "summary": "Gabriel announces to Mary that she will bear Jesus.", "characters": ["Mary", "Gabriel", "Jesus"], "locations": ["Nazareth"]},
    {"title": "Nativity of Jesus", "testament": "New", "summary": "Jesus is born in Bethlehem and laid in a manger.", "characters": ["Mary", "Joseph (NT)", "Jesus"], "locations": ["Bethlehem"]},
    {"title": "Visit of the Magi", "testament": "New", "summary": "Magi from the east worship the child Jesus with gifts.", "characters": ["Jesus", "Mary"], "locations": ["Bethlehem"]},
    {"title": "Baptism of Jesus", "testament": "New", "summary": "Jesus is baptized in the Jordan and publicly affirmed.", "characters": ["Jesus", "John the Baptist"], "locations": ["Jordan River"]},
    {"title": "Temptation in the Wilderness", "testament": "New", "summary": "Jesus resists temptation during forty days in the wilderness.", "characters": ["Jesus"], "locations": ["Judean Wilderness"]},
    {"title": "Sermon on the Mount", "testament": "New", "summary": "Jesus teaches disciples about kingdom righteousness.", "characters": ["Jesus", "Peter"], "locations": ["Galilee"]},
    {"title": "Calling of the Twelve", "testament": "New", "summary": "Jesus appoints twelve apostles for ministry.", "characters": ["Jesus", "Peter"], "locations": ["Galilee"]},
    {"title": "Feeding of the Five Thousand", "testament": "New", "summary": "Jesus multiplies loaves and fish for a great crowd.", "characters": ["Jesus", "Peter"], "locations": ["Galilee"]},
    {"title": "Walking on Water", "testament": "New", "summary": "Jesus walks on the sea and strengthens the disciples' faith.", "characters": ["Jesus", "Peter"], "locations": ["Galilee"]},
    {"title": "Transfiguration", "testament": "New", "summary": "Jesus is transfigured before selected disciples.", "characters": ["Jesus", "Peter"], "locations": ["Galilee"]},
    {"title": "Raising of Lazarus", "testament": "New", "summary": "Jesus raises Lazarus from the dead near Jerusalem.", "characters": ["Jesus", "Lazarus"], "locations": ["Jerusalem"]},
    {"title": "Triumphal Entry", "testament": "New", "summary": "Jesus enters Jerusalem as crowds welcome him.", "characters": ["Jesus"], "locations": ["Jerusalem"]},
    {"title": "Last Supper", "testament": "New", "summary": "Jesus shares Passover with disciples and institutes communion.", "characters": ["Jesus", "Peter"], "locations": ["Jerusalem"]},
    {"title": "Crucifixion", "testament": "New", "summary": "Jesus is crucified outside Jerusalem.", "characters": ["Jesus", "Mary"], "locations": ["Jerusalem"]},
    {"title": "Resurrection", "testament": "New", "summary": "Jesus rises from the dead on the third day.", "characters": ["Jesus", "Mary"], "locations": ["Jerusalem"]},
    {"title": "Great Commission", "testament": "New", "summary": "The risen Jesus sends disciples to all nations.", "characters": ["Jesus", "Peter"], "locations": ["Galilee"]},
    {"title": "Pentecost", "testament": "New", "summary": "The Holy Spirit empowers believers in Jerusalem.", "characters": ["Peter"], "locations": ["Jerusalem"]},
    {"title": "Conversion of Paul", "testament": "New", "summary": "Saul encounters the risen Christ on the road to Damascus.", "characters": ["Paul", "Jesus"], "locations": ["Damascus"]},
    {"title": "Peter and Cornelius", "testament": "New", "summary": "Peter visits Cornelius and sees Gentiles receive the Spirit.", "characters": ["Peter"], "locations": ["Caesarea"]},
    {"title": "Paul in Athens", "testament": "New", "summary": "Paul proclaims the gospel at the Areopagus.", "characters": ["Paul"], "locations": ["Athens"]},
]

CHARACTERS = {
    "God": "Creator in Genesis narrative.",
    "Adam": "First man in Genesis.",
    "Eve": "First woman in Genesis.",
    "Noah": "Builder of the ark and survivor of the flood.",
    "Nimrod": "Traditionally associated with Babel.",
    "Abraham": "Patriarch called by God to become father of many nations.",
    "Isaac": "Son of Abraham and Sarah; child of promise.",
    "Jacob": "Patriarch renamed Israel.",
    "Joseph": "Son of Jacob who rose to power in Egypt.",
    "Moses": "Leader of Israel in the exodus from Egypt.",
    "Pharaoh": "Ruler of Egypt during the exodus narrative.",
    "Joshua": "Successor to Moses and leader into Canaan.",
    "David": "Shepherd, king, and psalmist of Israel.",
    "Goliath": "Philistine champion defeated by David.",
    "Solomon": "King known for wisdom and temple building.",
    "Elijah": "Prophet who challenged Baal worship.",
    "Jonah": "Prophet sent to Nineveh.",
    "Daniel": "Exile known for faithful witness in Babylon.",
    "Ezra": "Priest and scribe active in post-exilic restoration.",
    "Nehemiah": "Governor who rebuilt Jerusalem's walls.",
    "Mary": "Mother of Jesus.",
    "Joseph (NT)": "Earthly father of Jesus.",
    "Jesus": "Central figure of the New Testament.",
    "Peter": "Disciple and apostolic leader in Jerusalem.",
    "Paul": "Apostle to the Gentiles.",
    "John the Baptist": "Prophet who baptized Jesus.",
    "Lazarus": "Man raised from the dead by Jesus.",
    "Gabriel": "Angel who announced Jesus' birth.",
}

LOCATIONS = {
    "Jerusalem": "Historic city central to many biblical events.",
    "Bethlehem": "Birthplace of David and Jesus.",
    "Nazareth": "Town in Galilee associated with Jesus' upbringing.",
    "Mount Sinai": "Traditional site of covenant and law giving.",
    "Babylon": "Major Mesopotamian city tied to exile.",
    "Galilee": "Region where much of Jesus' ministry occurred.",
    "Eden": "Garden where humanity's first story unfolds.",
    "Ararat": "Traditional resting place of Noah's ark.",
    "Hebron": "Patriarchal region associated with Abraham.",
    "Penuel": "Place where Jacob wrestled and was renamed.",
    "Egypt": "Land of Joseph's leadership and Israelite slavery.",
    "Red Sea": "Waters crossed during the exodus.",
    "Jericho": "Canaanite city captured under Joshua.",
    "Mount Carmel": "Site of Elijah's contest with prophets of Baal.",
    "Nineveh": "Assyrian city addressed by Jonah.",
    "Jordan River": "River where Jesus was baptized.",
    "Judean Wilderness": "Region of Jesus' temptation.",
    "Damascus": "City near Paul's conversion encounter.",
    "Caesarea": "Port city associated with Cornelius.",
    "Athens": "Greek city where Paul spoke at the Areopagus.",
}

ARTWORKS = [
    {"title": "The Creation of Adam", "artist": "Michelangelo", "year": 1512, "museum": "Sistine Chapel", "description": "Fresco depicting God giving life to Adam.", "related_story_title": "Creation"},
    {"title": "Noah's Ark", "artist": "Edward Hicks", "year": 1846, "museum": "Philadelphia Museum of Art", "description": "Folk rendering of Noah's ark narrative.", "related_story_title": "Noah and the Flood"},
    {"title": "Moses Breaking the Tablets of the Law", "artist": "Rembrandt", "year": 1659, "museum": "Gemäldegalerie, Berlin", "description": "Moses descends Sinai carrying the tablets.", "related_story_title": "Giving of the Law"},
    {"title": "David with the Head of Goliath", "artist": "Caravaggio", "year": 1610, "museum": "Galleria Borghese", "description": "Dramatic depiction of David's victory.", "related_story_title": "David and Goliath"},
    {"title": "The Sacrifice of Isaac", "artist": "Caravaggio", "year": 1603, "museum": "Uffizi Gallery", "description": "Angel intervenes in Abraham's test.", "related_story_title": "Binding of Isaac"},
    {"title": "The Annunciation", "artist": "Fra Angelico", "year": 1440, "museum": "Convent of San Marco", "description": "Gabriel announces Christ's birth to Mary.", "related_story_title": "Annunciation"},
    {"title": "The Nativity with the Prophets Isaiah and Ezekiel", "artist": "Duccio", "year": 1308, "museum": "National Gallery, London", "description": "Panel painting of Christ's birth.", "related_story_title": "Nativity of Jesus"},
    {"title": "The Last Supper", "artist": "Leonardo da Vinci", "year": 1498, "museum": "Santa Maria delle Grazie", "description": "Iconic mural of Jesus and the disciples.", "related_story_title": "Last Supper"},
    {"title": "The Crucifixion", "artist": "Diego Velázquez", "year": 1632, "museum": "Museo del Prado", "description": "Baroque depiction of the crucified Christ.", "related_story_title": "Crucifixion"},
    {"title": "The Resurrection of Christ", "artist": "Raphael", "year": 1502, "museum": "São Paulo Museum of Art", "description": "Christ rising triumphantly from the tomb.", "related_story_title": "Resurrection"},
]


def validate_seed_data() -> None:
    for story in STORY_SEEDS:
        if not story["characters"]:
            raise ValueError(f"Story '{story['title']}' has no characters")
        if not story["locations"]:
            raise ValueError(f"Story '{story['title']}' has no locations")

        for character in story["characters"]:
            if character not in CHARACTERS:
                raise ValueError(f"Story '{story['title']}' references unknown character '{character}'")

        for location in story["locations"]:
            if location not in LOCATIONS:
                raise ValueError(f"Story '{story['title']}' references unknown location '{location}'")

    story_titles = {story["title"] for story in STORY_SEEDS}
    for artwork in ARTWORKS:
        if artwork["related_story_title"] not in story_titles:
            raise ValueError(
                f"Artwork '{artwork['title']}' references unknown story '{artwork['related_story_title']}'"
            )


def populate_database() -> None:
    validate_seed_data()
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.executescript(schema_sql)

        conn.executemany(
            "INSERT INTO stories (title, testament, summary) VALUES (?, ?, ?)",
            [(story["title"], story["testament"], story["summary"]) for story in STORY_SEEDS],
        )
        conn.executemany(
            "INSERT INTO characters (name, description) VALUES (?, ?)",
            [(name, description) for name, description in CHARACTERS.items()],
        )
        conn.executemany(
            "INSERT INTO locations (name, description) VALUES (?, ?)",
            [(name, description) for name, description in LOCATIONS.items()],
        )

        story_ids = {title: story_id for story_id, title in conn.execute("SELECT id, title FROM stories")}
        character_ids = {name: character_id for character_id, name in conn.execute("SELECT id, name FROM characters")}
        location_ids = {name: location_id for location_id, name in conn.execute("SELECT id, name FROM locations")}

        conn.executemany(
            "INSERT INTO story_characters (story_id, character_id) VALUES (?, ?)",
            [
                (story_ids[story["title"]], character_ids[character])
                for story in STORY_SEEDS
                for character in story["characters"]
            ],
        )
        conn.executemany(
            "INSERT INTO story_locations (story_id, location_id) VALUES (?, ?)",
            [
                (story_ids[story["title"]], location_ids[location])
                for story in STORY_SEEDS
                for location in story["locations"]
            ],
        )

        artwork_rows = [
            (
                artwork["title"],
                artwork["artist"],
                artwork["year"],
                artwork["museum"],
                story_ids[artwork["related_story_title"]],
                artwork["description"],
            )
            for artwork in ARTWORKS
        ]
        conn.executemany(
            """
            INSERT INTO artworks (title, artist, year, museum, related_story_id, description)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            artwork_rows,
        )

        artwork_ids = {title: artwork_id for artwork_id, title in conn.execute("SELECT id, title FROM artworks")}
        conn.executemany(
            "INSERT INTO story_artworks (story_id, artwork_id) VALUES (?, ?)",
            [
                (story_ids[artwork["related_story_title"]], artwork_ids[artwork["title"]])
                for artwork in ARTWORKS
            ],
        )
        conn.commit()


if __name__ == "__main__":
    populate_database()
    print(f"Seeded database at {DB_PATH}")
