import tempfile
import unittest
from pathlib import Path
from pipeline import connect,load_fixture,ingest,list_channels,list_videos,annotate,stats

FIXTURE=Path(__file__).resolve().parents[1]/"fixtures"/"sample.json"

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.db=connect(Path(self.tmp.name)/"test.sqlite")

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def test_repeatable_import(self):
        load_fixture(self.db,FIXTURE)
        load_fixture(self.db,FIXTURE)
        self.assertEqual(stats(self.db),{"channels":2,"videos":3,"runs":2})

    def test_manual_notes_survive_updates(self):
        load_fixture(self.db,FIXTURE)
        self.assertTrue(annotate(self.db,"channel","fictional-c1","manual note"))
        self.assertTrue(annotate(self.db,"video","example-v1","product researched"))
        load_fixture(self.db,FIXTURE)
        self.assertEqual(next(x for x in list_channels(self.db) if x["id"]=="fictional-c1")["analyst_note"],"manual note")
        self.assertEqual(next(x for x in list_videos(self.db) if x["id"]=="example-v1")["product_note"],"product researched")

    def test_bad_video_rolls_back_entire_batch(self):
        with self.assertRaises(ValueError):
            ingest(self.db,{"channels":[{"id":"x","name":"name","subscribers":2,"category":"c"}],
                 "videos":[{"id":"x1","channel_id":"x","kind":"short","title":"bad","views":-1,"likes":0,"comments":0}]})
        self.assertEqual(stats(self.db),{"channels":0,"videos":0,"runs":0})

    def test_orphan_video_rejected(self):
        with self.assertRaises(sqlite3.IntegrityError):
            ingest(self.db,{"channels":[],"videos":[{"id":"v","channel_id":"missing","kind":"video",
                  "title":"t","views":0,"likes":0,"comments":0}]})

    def test_note_limit(self):
        with self.assertRaises(ValueError):
            annotate(self.db,"channel","x","a"*501)

import sqlite3

if __name__=="__main__":
    unittest.main()
