from flask import Flask, jsonify
import pandas as pd
import json
from sqlalchemy import create_engine
from flask_cors import CORS


from models.iss.iss import *
from models.risk.risk import *
from models.cal.cal import *
from viz.app import *







app = Flask(__name__)
CORS(app)



viz_url = [viz_d1, viz_d2, viz_d3, viz_d4, viz_d5, viz_d6, viz_d7]
models_url = [models_iss, models_risk, models_cal]

for i in viz_url :
	app.register_blueprint(i)

for i in models_url:
	app.register_blueprint(i)







@app.errorhandler(400)
def bad_request(error=None):
	message = {
			'status': 400,
			'message': 'Bad Request: ' + request.url + '--> Please check your data payload...',
	}
	resp = jsonify(message)
	resp.status_code = 400

	return responses





if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
