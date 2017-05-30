# SimpleHTTPDiary
Simple diary API implementation through a HTTP local web server


PREREQUISITES
------------------
1) Install latest python interpreter version 2.7.x
2) Install latest Flask compact web server (pip install flask)
3) Install latest Flask-RESTful REST extension package (pip install flask-restful)


USAGE
-----------
1) Runnig the application directly
1.1) Open a cmd console and run 'run_diary_app.sh' (NOTE: under linux you might need to grant the script execute permission 'sudo chmod 777 run_diary_app.sh')
1.2) Open another cmd console and follow the instructions below:

'''Usage - Diary Actions'''
## POST - Add new record
## GET - Search records by title/description and/or dates range
## PUT - Update records by title/desc and/or dates range with new title and/or description
## DELETE - Delete records by title/description and/or dates range

# curl http://127.0.0.1:5000/action -d "title=XXX" -d "desc=YYY" -d "date=d/m/yyyy" -X POST

# curl http://127.0.0.1:5000/action -d "title=XXX" -d "desc=YYY" -d "start=1-1-1900" -d "end=31-12-9999" -X GET/DELETE
# curl http://127.0.0.1:5000/action -d "title=XXX" -d "desc=YYY" -X GET/DELETE
# curl http://127.0.0.1:5000/action -d "start=1-1-1900" -d "end=31-12-9999" -X GET/DELETE

# curl http://127.0.0.1:5000/action -d "title=XXX" -d "desc=YYY" -d "start=1-1-1900" -d "end=31-12-9999" -d "newTitle=xXxX" -d "newDesc=yYyY" -X PUT
# curl http://127.0.0.1:5000/action -d "title=XXX" -d "desc=YYY" -d "newTitle=xXxX" -d "newDesc=yYyY" -X PUT
# curl http://127.0.0.1:5000/action -d "start=1-1-1900" -d "end=31-12-9999" -d "newTitle=xXxX" -d "newDesc=yYyY" -X PUT

# curl http://127.0.0.1:5000/action -d "title=XXX" -d "desc=YYY" -d "start=1-1-1900" -d "end=31-12-9999" -d "newTitle=xXxX" -X PUT
# curl http://127.0.0.1:5000/action -d "title=XXX" -d "desc=YYY" -d "newTitle=xXxX" -X PUT
# curl http://127.0.0.1:5000/action -d "start=1-1-1900" -d "end=31-12-9999" -d "newTitle=xXxX" -X PUT

# curl http://127.0.0.1:5000/action -d "title=XXX" -d "desc=YYY" -d "start=1-1-1900" -d "end=31-12-9999" -d "newDesc=yYyY" -X PUT
# curl http://127.0.0.1:5000/action -d "title=XXX" -d "desc=YYY" -d "newDesc=yYyY" -X PUT
# curl http://127.0.0.1:5000/action -d "start=1-1-1900" -d "end=31-12-9999" -d "newDesc=yYyY" -X PUT


'''Usage - Diary Backup'''
## GET - Save diary data to a local backup .json file
## POST - Load data from local .json backup file to the programs diary data structure

# curl http://127.0.0.1:5000/backup -X GET
# curl http://127.0.0.1:5000/backup -X POST


2) Running the application's tests:
- Open a cmd console and run the 'run_diary_tests.sh' script (NOTE: under linux you might need to grant the script execute permission 'sudo chmod 777 run_diary_tests.sh')
- The test progress will be displayed during the tests execution