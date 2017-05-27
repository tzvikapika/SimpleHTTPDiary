import datetime
from flask import Flask
from flask import request
from flask_restful import Api
from flask_restful import Resource


app = Flask(__name__)
api = Api(app)

record_id = 0
diary = list(dict())

class DiaryAction(Resource):
    def get(self):
        desc = request.form.get('desc')
        start = request.form.get('start')
        end = request.form.get('end')

        if desc is None and start is None and end is None:
            return "Insufficient Input, <desc> or/and <start> <end> expected"
        if desc is not None and desc == "":
            return "Invalid Input, <desc> can not be empty"
        if start is None and end is not None:
            return "Insufficient Input, <start> expected"
        if start is not None and end is None:
            return "Insufficient Input, <end> expected"

        recordsByDesc = list(dict())
        if desc is not None:
            for rec in diary:
                recDesc = rec['desc']
                if desc in recDesc: # TODO: the comparison is case sensitive, needs fix
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

        if desc is not None and start is not None and end is not None:
            commonRecords = list(dict())
            for rec in recordsByDesc:
                if rec in recordsByDate:
                    commonRecords.append(rec)
            return commonRecords
        elif desc is not None:
            return recordsByDesc
        else:
            return recordsByDate


    def put(self):
        
        pass


    def post(self):
        date = request.form.get('date')
        title = request.form.get('title')
        desc = request.form.get('desc')

        if date is None or title is None or desc is None:
            return "Insufficient Input, <date> <title> <desc> expected"
        if title == "" or desc == "":
            return "Invalid Input, <title> <desc> can not be empty"

        try:
            dt = datetime.datetime.strptime(date, "%d-%m-%Y").date()
            date = dt.strftime("%d-%m-%Y")
        except ValueError as ex:
            return str(ex)

        global record_id
        diary.append({"id":record_id, "date":date, "title":title, "desc":desc})
        record_id += 1
        return "\nAdded new entry"


    def delete(self):
        data = request.form.get('date')
        pass


class DiaryBackup(Resource):
    def get(self):
        pass

    def post(self):
        pass

api.add_resource(DiaryAction, '/action')
api.add_resource(DiaryBackup, '/backup')

if __name__ == "__main__":
    app.run(debug=True)


'''Usage'''
# curl http://127.0.0.1:5000/action -d "desc=" -d "start=" -d "end=" -X GET
# curl http://127.0.0.1:5000/action -d "desc=" -X GET
# curl http://127.0.0.1:5000/action -d "start=" -d "end=" -X GET

# curl http://127.0.0.1:5000/action -d "date=" -d "title=" -d "desc=" -X POST

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


'''Teardown'''
# Save results
# Tests residue cleanup
# Dispose of resources



# Make full use cases if time is left