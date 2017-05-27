import unittest
import SimpleHTTPDiary

class SimpleHTTPDiary_Tests(unittest.TestCase):
    def setUp(self):
        SimpleHTTPDiary.app.config['TESTING'] = True
        self.app = SimpleHTTPDiary.app.test_client()
        SimpleHTTPDiary.app.test_client()
        print self.id()

    def tearDown(self):
        del SimpleHTTPDiary.diary[:]

    def test_addRecord_missing_args(self):
        response = self.app.post("/action", data = dict({"title": "", "desc": ""}))
        self.assertTrue("Insufficient Input, <date> <title> <desc> expected" in response.data)
        response = self.app.post("/action", data=dict({"date": "", "desc": ""}))
        self.assertTrue("Insufficient Input, <date> <title> <desc> expected" in response.data)
        response = self.app.post("/action", data=dict({"date": "", "title": ""}))
        self.assertTrue("Insufficient Input, <date> <title> <desc> expected" in response.data)
        self.assertTrue(len(SimpleHTTPDiary.diary) == 0)

    def test_addRecord_title_desc_empty(self):
        response = self.app.post("/action", data = dict({"date": "1-1-1900", "title":"", "desc": "someDesc1"}))
        self.assertTrue("Invalid Input, <title> <desc> can not be empty" in response.data)
        response = self.app.post("/action", data=dict({"date": "1-1-1900", "title": "someTitle1", "desc": ""}))
        self.assertTrue("Invalid Input, <title> <desc> can not be empty" in response.data)
        self.assertTrue(len(SimpleHTTPDiary.diary) == 0)

    def test_addRecord_invalid_date(self):
        response = self.app.post("/action", data = dict({"date": "99-99-99999", "title": "someTitle1", "desc": "someDesc1"}))
        self.assertTrue("does not match format '%d-%m-%Y'" in response.data)
        response = self.app.post("/action", data=dict({"date": "1-1-19999", "title": "someTitle1", "desc": "someDesc1"}))
        self.assertTrue("unconverted data remains:" in response.data)
        self.assertTrue(len(SimpleHTTPDiary.diary) == 0)




if __name__ == '__main__':
    unittest.main()