"""New, clean-room synthetic channel + video pipeline. Never fetches real data."""
import json
import sqlite3
from pathlib import Path

def connect(path=":memory:"):
    db=sqlite3.connect(str(path),check_same_thread=False)
    db.row_factory=sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    db.executescript("""
    CREATE TABLE IF NOT EXISTS channels(
        id TEXT PRIMARY KEY, name TEXT NOT NULL, subscribers INTEGER NOT NULL,
        category TEXT NOT NULL, audience TEXT NOT NULL, analyst_note TEXT DEFAULT '');
    CREATE TABLE IF NOT EXISTS videos(
        id TEXT PRIMARY KEY, channel_id TEXT NOT NULL REFERENCES channels(id),
        kind TEXT NOT NULL CHECK(kind IN ('video','short')),
        title TEXT NOT NULL, views INTEGER NOT NULL CHECK(views>=0),
        likes INTEGER NOT NULL CHECK(likes>=0), comments INTEGER NOT NULL CHECK(comments>=0),
        product_note TEXT DEFAULT '');
    CREATE TABLE IF NOT EXISTS runs(id INTEGER PRIMARY KEY AUTOINCREMENT,
        channels_loaded INTEGER NOT NULL, videos_loaded INTEGER NOT NULL);
    """)
    db.commit()
    return db

def positive(record,key):
    value=record[key]
    if isinstance(value,bool) or not isinstance(value,int) or value<0:
        raise ValueError(key+" must be non-negative integer")
    return value

def txt(record,key):
    value=record[key]
    if not isinstance(value,str) or not value.strip():
        raise ValueError(key+" must be non-empty text")
    return value.strip()

def ingest(db,payload):
    if not isinstance(payload,dict) or not isinstance(payload.get("channels"),list) \
        or not isinstance(payload.get("videos"),list):
        raise ValueError("Expected channels and videos lists")
    with db:
        for c in payload["channels"]:
            db.execute("""INSERT INTO channels(id,name,subscribers,category,audience)
                VALUES(?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET
                name=excluded.name,subscribers=excluded.subscribers,
                category=excluded.category,audience=excluded.audience""",
                (txt(c,"id"),txt(c,"name"),positive(c,"subscribers"),
                txt(c,"category"),json.dumps(c.get("audience",{}),sort_keys=True)))
        for v in payload["videos"]:
            kind=txt(v,"kind")
            if kind not in ("short","video"):
                raise ValueError("unsupported video kind")
            db.execute("""INSERT INTO videos(id,channel_id,kind,title,views,likes,comments)
                VALUES(?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET
                channel_id=excluded.channel_id,kind=excluded.kind,title=excluded.title,
                views=excluded.views,likes=excluded.likes,comments=excluded.comments""",
                (txt(v,"id"),txt(v,"channel_id"),kind,txt(v,"title"),positive(v,"views"),
                positive(v,"likes"),positive(v,"comments")))
        db.execute("INSERT INTO runs(channels_loaded,videos_loaded) VALUES(?,?)",
                   (len(payload["channels"]),len(payload["videos"])))
    return stats(db)

def load_fixture(db,file):
    return ingest(db,json.loads(Path(file).read_text(encoding="utf-8")))

def list_channels(db):
    rows=[dict(x) for x in db.execute("SELECT * FROM channels ORDER BY subscribers DESC,id")]
    for row in rows:
        row["audience"]=json.loads(row["audience"])
    return rows

def list_videos(db):
    return [dict(x) for x in db.execute("SELECT * FROM videos ORDER BY channel_id,views DESC")]

def annotate(db,kind,code,note):
    if len(note)>500:
        raise ValueError("note too long")
    mapping={"channel":("channels","analyst_note"),"video":("videos","product_note")}
    if kind not in mapping:
        raise ValueError("unknown entity")
    table,field=mapping[kind]
    with db:
        return db.execute("UPDATE "+table+" SET "+field+"=? WHERE id=?",
                          (note,code)).rowcount>0

def stats(db):
    return {label: db.execute("SELECT COUNT(*) FROM "+table).fetchone()[0]
            for label,table in (("channels","channels"),("videos","videos"),("runs","runs"))}
