import datetime
import types
import json
from flask import Flask
from flask import request
from flask_restful import Api
from flask_restful import Resource

app = Flask(__name__)
api = Api(app)

diary = list(dict())
BACKUP_FILE = "./diaryBackup"

def Search(title = None, desc = None, start = None, end = None):
    if title is None and desc is None and start is None and end is None: # No-arguments check
        return "Insufficient Input, <title> <desc> or/and <start> <end> expected"
    if (title is not None and title == "") or (desc is not None and desc == ""): # title/desc can't be empty
        return "Invalid Input, <title> <desc> can not be empty"
    if (title is None and desc is not None) or (title is not None and desc is None): # title and desc always paired
        return "Insufficient Input, <title> <desc> expected"
    if (start is None and end is not None) or (start is not None and end is None): # start and end always paired
        return "Insufficient Input, <start> <end> expected"

    recordsByDesc = list(dict())
    if desc is not None:
        for rec in diary:
            recTitle = rec['title']
            recDesc = rec['desc']
            if str(title).lower() in str(recTitle).lower() and str(desc).lower() in str(recDesc).lower():
                recordsByDesc.append(rec)

    recordsByDate = list(dict())
    if start is not None and end is not None:
        try:
            dt1 = datetime.datetime.strptime(start, "%d-%m-%Y").date()
            dt2 = datetime.datetime.strptime(end, "%d-%m-%Y").date()
        except ValueError as ex:
            return str(ex)

        if dt1 > dt2:
            return "Start date can not be greater than End date"

        for rec in diary:
            recDate = datetime.datetime.strptime(dict(rec)['date'], "%d-%m-%Y").date()
            if recDate >= dt1 and recDate <= dt2:
                recordsByDate.append(rec)

    if title is not None and desc is not None and start is not None and end is not None:
        commonRecords = list(dict())
        for rec in recordsByDesc:
            if rec in recordsByDate:
                commonRecords.append(rec)
        return commonRecords
    elif title is not None and desc is not None:
        return recordsByDesc
    else:
        return recordsByDate


class DiaryAction(Resource):
    def get(self): # Get a list of events by title-desc or/and date range
        title = request.form.get('title')
        desc = request.form.get('desc')
        start = request.form.get('start')
        end = request.form.get('end')

        result = Search(title, desc, start, end)
        if not isinstance(result, types.ListType):
            return result

        return result


    def put(self): # Update events by title-desc or/and date range
        title = request.form.get('title')
        desc = request.form.get('desc')
        start = request.form.get('start')
        end = request.form.get('end')

        newTitle = request.form.get('newTitle')
        newDesc = request.form.get('newDesc')

        if newTitle is None and newDesc is None:
            return "Insufficient Input, <newTitle> or/and <newDesc> expected"
        if (newTitle is not None and newTitle == "") or (newDesc is not None and newDesc == ""):
            return "Invalid Input, <newTitle> <newDesc> can not be empty"

        result = Search(title, desc, start, end)
        if not isinstance(result, types.ListType):
            return result

        for rec in result:
            if newTitle is not None:
                rec['title'] = newTitle
            if newDesc is not None:
                rec['desc'] = newDesc
        return result


    def post(self): # Add new events with date, title and desc
        date = request.form.get('date')
        title = request.form.get('title')
        desc = request.form.get('desc')

        if date is None or title is None or desc is None: # Mandatory args check
            return "Insufficient Input, <date> <title> <desc> expected"
        if title == "" or desc == "":
            return "Invalid Input, <title> <desc> can not be empty"

        try:
            dt = datetime.datetime.strptime(date, "%d-%m-%Y").date()
            date = dt.strftime("%d-%m-%Y")
        except ValueError as ex:
            return str(ex)

        diary.append({"date":date, "title":title, "desc":desc})
        return "Added new entry"


    def delete(self): # Delete events by title-desc or/and date range
        title = request.form.get('title')
        desc = request.form.get('desc')
        start = request.form.get('start')
        end = request.form.get('end')

        result = Search(title, desc, start, end)
        if not isinstance(result, types.ListType):
            return result

        for rec in result:
            diary.remove(rec)
        return result

class DiaryBackup(Resource):
    def get(self): # Save backup to file
        global diary
        fp = open(BACKUP_FILE, "w")
        json.dump(diary, fp)
        fp.close()
        return "Backup saved"

    def post(self): # Load backup from file
        global diary

        try:
            fp = open(BACKUP_FILE, "r")
        except IOError as ex:
            return str(ex)

        diary = json.load(fp)
        fp.close()
        return "Backup loaded"

api.add_resource(DiaryAction, '/action')
api.add_resource(DiaryBackup, '/backup')

if __name__ == "__main__":
    app.run(debug=True)


'''Usage'''
# curl http://127.0.0.1:5000/action -d "title=XXX" -d "desc=YYY" -d "start=1-1-1900" -d "end=31-12-9999" -X GET/PUT/DELETE
# curl http://127.0.0.1:5000/action -d "title=XXX" -d "desc=YYY" -X GET/PUT/DELETE
# curl http://127.0.0.1:5000/action -d "start=1-1-1900" -d "end=31-12-9999" -X GET/PUT/DELETE

# curl http://127.0.0.1:5000/action -d "title=" -d "desc=" -d "date=" -X POST

'''Setup'''
# Check for data structure
# Check for initialized ID counter
# Check for accessible local filesystem

'''POST unit tests'''
# Add new entry - check added (out + dict)
# Add unique id increment check + check all records have unique id after multiple operations
# Ommit intrinsic parameters/supply wrong parameters
# Supply invalid date values (e.g. 99-99-99, 01-01-99, !@#$%^&*)
# Check for empty titles/descs in records

'''GET unit tests'''
# Get single existing entry - key/value correlate each other correctly including content
# Get multiple entries by range of dates, check correct count of records
# Get single entry that doesn't exist
# Get range of entries that don't exist
# Ommit intrinsic parameters/supply wrong parameters + Ommit all parameters
# Serach only by desc
# Search only by date
# search by desc and date
# Supply invalid date values (e.g. 99-99-99, 01-01-99, 1-1-20000 !@#$%^&*)
# Supply invalid date ranges (start > end)
# Supply desc as empty string
# Test search with case sensitive description (if case affects the search results)

'''PUT unit tests'''
# Check for empty titles/descs in records
# Reconrd cnt after update
# Target records update sucess

"""DELETE"""
# Selected records deleted
# Non selected records are intact

'''Teardown'''
# Save results
# Tests residue cleanup
# Dispose of resources



# Make full use cases if time is left