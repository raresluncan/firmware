from repository import init_db
from firmware import app


print 'bang!'

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print("Firmware initialized database sucessfully!")
