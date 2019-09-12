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


@app.route('/tracker', methods=['GET'])
def tracker_health():
    response = jsonify(healthResponse)
    return make_response(response, 200)


@app.route('/tracker/bulk', methods=['GET'])
def tracker_bulk():
    # 1. Goes through all the ids, starting from id = 1 
    #    up to a point where the API no longer returns data
    # 2. Does the same steps as the above function
    # 
    # Note: High chance there will not be a response. The response will be in a log.
    return make_response("Done", 200)