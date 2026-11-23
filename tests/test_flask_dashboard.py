import tempfile
import unittest
from pathlib import Path
from pipeline import connect,load_fixture
try:
    from app import create_app
except ImportError:
    create_app=None

FIXTURE=Path(__file__).resolve().parents[1]/"fixtures"/"sample.json"

@unittest.skipIf(create_app is None,"Flask not installed")
class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.path=Path(self.temp.name)/"app.sqlite"
        db=connect(self.path)
        load_fixture(db,FIXTURE)
        db.close()
        self.client=create_app(self.path).test_client()

    def tearDown(self):
        self.temp.cleanup()

    def test_screen_and_json(self):
        resp=self.client.get("/")
        self.assertEqual(resp.status_code,200)
        self.assertIn(b"Example Cooking Channel",resp.data)
        self.assertEqual(self.client.get("/api/summary").get_json()["videos"],3)

    def test_manual_note(self):
        self.assertEqual(self.client.post("/note/channel/fictional-c1",data={"note":"Checked"}).status_code,302)
        data=self.client.get("/api/channels").get_json()
        self.assertEqual(next(c for c in data if c["id"]=="fictional-c1")["analyst_note"],"Checked")

    def test_invalid_note(self):
        self.assertEqual(self.client.post("/note/channel/no-id",data={"note":"x"}).status_code,404)
        self.assertEqual(self.client.post("/note/video/example-v1",data={"note":"a"*501}).status_code,400)

if __name__=="__main__":
    unittest.main()
