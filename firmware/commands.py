"""COMMANDS FROM FIRMAREW SERVICE"""

from firmware.repository import init_db
from firmware import app

@app.cli.command('initdb')
def initdb_command():
    """ command to initialise the database if it doesnt laready exist """
    init_db()
    print "Firmware initialized database sucessfully!"
