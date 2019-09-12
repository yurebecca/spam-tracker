import os
import re
import json
import time
import copy
import requests
import logging
from flask import jsonify, make_response
from api import app
from api.tracker import SpamTracker as ST

API_TIMEOUT = 1
healthResponse = {
    "meta": {
        "message": 'Hello, World! Tracker is online!'
    }
}

st = ST.SpamTracker()

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
    endpoint = os.getenv("API_ENDPOINT") or "https://example.com/"
    url = endpoint + 'projects/'
    headers = {
        'authorization': 'Bearer ' + os.getenv("API_TOKEN")
    }
    responseData = []

    project_id = 1
    can_continue = True
    while can_continue:
        response = requests.get(url + f"{project_id}", headers = headers)

        logging.debug("hewwwoooo")
        if response.status_code == 200:
            response_json = response.json()

            # Append all the text fields
            content = " ".join([
                response_json["project"]["name"],
                response_json["project"]["blurb"],
                response_json["project"]["description"]
            ])
            milestone_content = list()
            for m in response_json["project"]["milestones"]:
                milestone_content.append(m["name"])
                milestone_content.append(m["description"])
            content += " " + " ".join(milestone_content)

            # Clean the content as needed
            content = re.sub(r"\n+", " ", content)
            content = content.replace("*", "")
            # print(content)

            st.reset()
            st.set_content(content)
            st.predict()

            responseData.append(
                {
                    "project_id": project_id,
                    "severity_rating": st.final_rating(),
                    "severity_type": st.severity_type
                }
            )

            project_id += 1
            time.sleep(API_TIMEOUT)
        elif response.status_code == 404:
            # Assume that the data in the db has not been tampered with
            can_continue = False


    response = jsonify(responseData)
    return make_response(response, 200)
    return make_response("Done", 200)