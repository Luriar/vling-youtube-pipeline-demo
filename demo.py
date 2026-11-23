"""Clean-room fake-data pipeline illustrating upsert/annotation preservation."""
import sqlite3

def connect():
    db=sqlite3.connect(":memory:")
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("""CREATE TABLE channels(
        id TEXT PRIMARY KEY, name TEXT NOT NULL, subscribers INTEGER,
        manual_note TEXT DEFAULT '')""")
    db.execute("""CREATE TABLE videos(
        id TEXT PRIMARY KEY, channel_id TEXT NOT NULL,
        kind TEXT NOT NULL, views INTEGER NOT NULL,
        FOREIGN KEY(channel_id) REFERENCES channels(id))""")
    db.commit()
    return db

def import_channel(db, code, name, subscribers):
    with db:
        db.execute("""INSERT INTO channels(id,name,subscribers)
           VALUES(?,?,?) ON CONFLICT(id) DO UPDATE
           SET name=excluded.name, subscribers=excluded.subscribers""",
           (code,name,subscribers))

def annotate_channel(db, code, note):
    with db:
        db.execute("UPDATE channels SET manual_note=? WHERE id=?",(note,code))

def import_video(db, code, channel, kind, views):
    if kind not in ("video","short"):
        raise ValueError("unsupported kind")
    with db:
        db.execute("""INSERT INTO videos(id,channel_id,kind,views) VALUES(?,?,?,?)
           ON CONFLICT(id) DO UPDATE SET views=excluded.views,kind=excluded.kind""",
           (code,channel,kind,views))

def channels(db):
    return db.execute("SELECT id,name,subscribers,manual_note FROM channels ORDER BY id").fetchall()

def videos(db):
    return db.execute("SELECT id,channel_id,kind,views FROM videos ORDER BY id").fetchall()

if __name__ == "__main__":
    db=connect()
    import_channel(db,"fictional-1","Example Creator",2500)
    annotate_channel(db,"fictional-1","Manual research note")
    import_channel(db,"fictional-1","Example Creator Updated",2800)
    import_video(db,"video-1","fictional-1","short",120)
    print(channels(db),videos(db))
