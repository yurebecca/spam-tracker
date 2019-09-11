from flask import jsonify, make_response
from api import app

healthResponse = {
    "meta": {
        "message": 'Tracker is online!'
    }
}

@app.route('/tracker', methods=['GET'])
def tracker_health():
    response = jsonify(healthResponse)
    return make_response(response, 200)


@app.route('/tracker/<project_id>', methods=['GET'])
def tracker_by_project_id(project_id):
    # 1. Call API to get project details
    # 2. Get all text fields from the project and run through the tests for
    #   a. Profanity
    #   b. Keyword Stuffing
    #   c. Spam (shsould include those of Viagra sales)
    #   d. Short Projects? (based on wordcount maybe?)
    return make_response("Done", 200)


@app.route('/tracker/bulk', methods=['GET'])
def tracker_bulk():
    # 1. Goes through all the ids, starting from id = 1 
    #    up to a point where the API no longer returns data
    # 2. Does the same steps as the above function
    # 
    # Note: High chance there will not be a response. The response will be in a log.
    return make_response("Done", 200)