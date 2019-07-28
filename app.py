from flask import Flask

import models

DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

app = Flask(__name__)


@app.route('/')
def hello_world():
	return 'Hello World!'


if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, host=HOST, port=PORT)
