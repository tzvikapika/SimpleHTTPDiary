import unittest
import SimpleHTTPDiary

class SimpleHTTPDiary_Tests(unittest.TestCase):
    def sendHttpRequest(self, api='/action', dataDict=dict(), method='GET'): # TODO: Integrate in tests
        resp = None
        if method == 'GET':
            resp = self.app.get(api, data=dataDict)
        if method == 'POST':
            resp = self.app.post(api, data=dataDict)
        if method == 'PUT':
            resp = self.app.put(api, data=dataDict)
        if method == 'DELETE':
            resp = self.app.delete(api, data=dataDict)
        self.assertTrue(resp.status == '200 OK', msg=resp.status)
        print str(resp)
        return resp.data

    def initAppData(self):
        SimpleHTTPDiary.diary.append({"date": "01-01-1900", "title": "someTitle1", "desc": "someDesc1"})
        SimpleHTTPDiary.diary.append({"date": "31-12-9999", "title": "someTitle2", "desc": "someDesc2"})
        SimpleHTTPDiary.diary.append({"date": "11-03-2001", "title": "someTitle3", "desc": "someDesc3"})
        SimpleHTTPDiary.diary.append({"date": "23-07-2001", "title": "someTitle4", "desc": "someDesc4"})
        SimpleHTTPDiary.diary.append({"date": "10-07-2001", "title": "someTitle5", "desc": "someDesc5"})
        SimpleHTTPDiary.diary.append({"date": "07-10-2010", "title": "someTitle6", "desc": "someDesc6"})

    def setUp(self):
        SimpleHTTPDiary.app.config['TESTING'] = True
        self.app = SimpleHTTPDiary.app.test_client()
        print self.id()

    def tearDown(self):
        del SimpleHTTPDiary.diary[:]


    ########################## Tests for adding new diary records functionality ##########################
    def test_addRecord_missing_date(self):
        response = self.app.post("/action", data = dict({"title": "", "desc": ""}))
        self.assertTrue("Insufficient Input, <date> <title> <desc> expected" in response.data)
        self.assertTrue(len(SimpleHTTPDiary.diary) == 0)

    def test_addRecord_missing_title(self):
        response = self.app.post("/action", data=dict({"date": "", "desc": ""}))
        self.assertTrue("Insufficient Input, <date> <title> <desc> expected" in response.data)
        self.assertTrue(len(SimpleHTTPDiary.diary) == 0)

    def test_addRecord_missing_desc(self):
        response = self.app.post("/action", data=dict({"date": "", "title": ""}))
        self.assertTrue("Insufficient Input, <date> <title> <desc> expected" in response.data)
        self.assertTrue(len(SimpleHTTPDiary.diary) == 0)

    def test_addRecord_empty_title(self):
        response = self.app.post("/action", data = dict({"date": "1-1-1900", "title":"", "desc": "someDesc1"}))
        self.assertTrue("Invalid Input, <title> <desc> can not be empty" in response.data)
        self.assertTrue(len(SimpleHTTPDiary.diary) == 0)

    def test_addRecord_empty_desc(self):
        response = self.app.post("/action", data=dict({"date": "1-1-1900", "title": "someTitle1", "desc": ""}))
        self.assertTrue("Invalid Input, <title> <desc> can not be empty" in response.data)
        self.assertTrue(len(SimpleHTTPDiary.diary) == 0)

    def test_addRecord_invalid_date_format(self):
        response = self.app.post("/action", data = dict({"date": "!@$23&*jhsdJWEG", "title": "someTitle1", "desc": "someDesc1"}))
        self.assertTrue("does not match format '%d-%m-%Y'" in response.data)
        self.assertTrue(len(SimpleHTTPDiary.diary) == 0)

    def test_addRecord_invalid_date_length(self):
        response = self.app.post("/action", data=dict({"date": "1-1-19999", "title": "someTitle1", "desc": "someDesc1"}))
        self.assertTrue("unconverted data remains:" in response.data)
        self.assertTrue(len(SimpleHTTPDiary.diary) == 0)

    def test_addRecord_invalid_date_yearOutOfRange(self):
        response = self.app.post("/action", data=dict({"date": "1-1-1899", "title": "someTitle1", "desc": "someDesc1"}))
        self.assertTrue("year=1899 is before 1900; the datetime strftime() methods require year >= 1900" in response.data)
        self.assertTrue(len(SimpleHTTPDiary.diary) == 0)

    def test_addRecord_newEntry_minDate(self):
        newRec = {"date":"01-01-1900", "title":"someTitle1", "desc":"someDesc1"}
        response = self.app.post("/action", data = newRec)
        self.assertTrue("Added new entry" in response.data)
        self.assertTrue(SimpleHTTPDiary.diary[0]["date"] == "01-01-1900" and
                        SimpleHTTPDiary.diary[0]["title"] == "someTitle1" and
                        SimpleHTTPDiary.diary[0]["desc"] == "someDesc1")
        self.assertTrue(len(SimpleHTTPDiary.diary) == 1)

    def test_addRecord_newEntry_maxDate(self):
        newRec = {"date":"31-12-9999", "title":"someTitle1", "desc":"someDesc1"}
        response = self.app.post("/action", data=newRec)
        self.assertTrue("Added new entry" in response.data)
        self.assertTrue(SimpleHTTPDiary.diary[0]["date"] == "31-12-9999" and
                        SimpleHTTPDiary.diary[0]["title"] == "someTitle1" and
                        SimpleHTTPDiary.diary[0]["desc"] == "someDesc1")
        self.assertTrue(len(SimpleHTTPDiary.diary) == 1)


    ########################## Tests for displaying existing diary records functionality ##########################
    def test_displayRecords_no_args(self):
        requestData = {}
        response = self.app.get("/action", data=requestData)
        self.assertTrue("Insufficient Input, <title> <desc> or/and <start> <end> expected" in response.data)

    def test_displayRecords_empty_title(self):
        requestData = {"title": "", "desc": "someDesc1"}
        response = self.app.get("/action", data=requestData)
        self.assertTrue("Invalid Input, <title> <desc> can not be empty" in response.data)

    def test_displayRecords_empty_desc(self):
        requestData = {"title": "someTitle1", "desc": ""}
        response = self.app.get("/action", data=requestData)
        self.assertTrue("Invalid Input, <title> <desc> can not be empty" in response.data)

    def test_displayRecords_missing_title(self):
        requestData = {"desc": "someDesc1"}
        response = self.app.get("/action", data=requestData)
        self.assertTrue("Insufficient Input, <title> <desc> expected" in response.data)

    def test_displayRecords_missing_desc(self):
        requestData = {"title": "someTitle1"}
        response = self.app.get("/action", data=requestData)
        self.assertTrue("Insufficient Input, <title> <desc> expected" in response.data)

    def test_displayRecords_missing_start(self):
        requestData = {"end": ""}
        response = self.app.get("/action", data=requestData)
        self.assertTrue("Insufficient Input, <start> <end> expected" in response.data)

    def test_displayRecords_missing_end(self):
        requestData = {"start": ""}
        response = self.app.get("/action", data=requestData)
        self.assertTrue("Insufficient Input, <start> <end> expected" in response.data)

    def test_displayRecords_invalid_start_date_format(self):
        requestData = {"start": "!@$23&*jhsdJWEG", "end":"31-12-9999", "title": "someTitle1", "desc": "someDesc1"}
        response = self.app.get("/action", data=requestData)
        self.assertTrue("does not match format '%d-%m-%Y'" in response.data)

    def test_displayRecords_invalid_start_date_length(self):
        requestData = {"start": "31-12-99999", "end":"31-12-9999", "title": "someTitle1", "desc": "someDesc1"}
        response = self.app.get("/action", data=requestData)
        self.assertTrue("unconverted data remains:" in response.data)

    def test_displayRecords_invalid_end_date_format(self):
        requestData = {"start": "31-12-9999", "end": "!@$23&*jhsdJWEG", "title": "someTitle1", "desc": "someDesc1"}
        response = self.app.get("/action", data=requestData)
        self.assertTrue("does not match format '%d-%m-%Y'" in response.data)

    def test_displayRecords_invalid_end_date_length(self):
        requestData = {"start": "31-12-9999", "end": "31-12-99999", "title": "someTitle1", "desc": "someDesc1"}
        response = self.app.get("/action", data=requestData)
        self.assertTrue("unconverted data remains:" in response.data)

    def test_displayRecords_date_start_greater_than_end(self):
        requestData = {"start": "31-12-9999", "end": "1-1-1900", "title": "someTitle1", "desc": "someDesc1"}
        response = self.app.get("/action", data=requestData)
        self.assertTrue("Start date can not be greater than End date" in response.data)

    def test_displayRecords_invalid_start_date_yearOutOfRange(self):
        requestData = {"start": "31-12-1899", "end": "1-1-1900", "title": "someTitle1", "desc": "someDesc1"}
        response = self.app.get("/action", data=requestData)
        self.assertTrue("year=1899 is before 1900; the datetime strftime() methods require year >= 1900" in response.data)

    def test_displayRecords_invalid_end_date_yearOutOfRange(self):
        requestData = {"start": "31-12-1900", "end": "1-1-1899", "title": "someTitle1", "desc": "someDesc1"}
        response = self.app.get("/action", data=requestData)
        self.assertTrue("year=1899 is before 1900; the datetime strftime() methods require year >= 1900" in response.data)
    # All the above 'displayRecords' tests check common functionality to GET/PUT/DELETE which is implemented within SimpleHTTPDiary.Search() func #

    def test_displayRecords_by_title_desc(self):
        self.initAppData()
        pass

    def test_displayRecords_by_start_end(self):
        pass

    def test_displayRecords_by_title_desc_start_end(self):
        pass


    ########################## Tests for updating existing diary records functionality ##########################
    def test_updateRecords_xyz(self):
        pass

    ########################## Tests for deleting existing diary records functionality ##########################
    def test_deleteRecords_xyz(self):
        pass

    ########################## Tests for saving diary backup ##########################
    def test_saveRecordsBackup_xyz(self):
        pass

    ########################## Tests for loading diary from backup ##########################
    def test_loadRecordsBackup_xyz(self):
        pass

if __name__ == '__main__':
    unittest.main()


# TODO: Integrate sendHttpRequest() method
# TODO: Implement test response data output / logger
# TODO: Implement common assert function with extended functionality