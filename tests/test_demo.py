import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import unittest
from demo import connect,import_channel,import_video,annotate_channel,channels,videos

class PipelineTests(unittest.TestCase):
    def test_manual_note_survives_upsert(self):
        db=connect()
        import_channel(db,"x","Before",10)
        annotate_channel(db,"x","keep me")
        import_channel(db,"x","After",20)
        self.assertEqual(channels(db)[0],("x","After",20,"keep me"))
        import_video(db,"v","x","short",50)
        import_video(db,"v","x","short",60)
        self.assertEqual(videos(db),[("v","x","short",60)])
        db.close()

if __name__ == "__main__":
    unittest.main()
