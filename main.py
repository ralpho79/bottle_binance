import sqlite3
from bottle import route, run, error, template, request
import bottle_app

run(host='localhost', port=8080, debug=True, reloader=True)