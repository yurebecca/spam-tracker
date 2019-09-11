from flask import jsonify, make_response
from api import app

healthResponse = {
    "meta": {
        "message": 'Hello, World! Tracker is online!'
    }
}

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    responseData = healthResponse
    response = jsonify(responseData)
    return make_response(response, 200)


from api import tracker