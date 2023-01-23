from bottle import run
import bottle_app

run(host='localhost', port=8080, debug=True, reloader=True)
