import os
import pandas as pd
import pickle
from flask import Flask, jsonify, request, Blueprint
import random
from flask_cors import CORS
from sqlalchemy import create_engine
import config



path = "models/risk/"

app = Flask(__name__)
CORS(app)

DB_CONNECT_STRING = "mysql+pymysql://" + config.credentials["username"]+ ":"+config.credentials["password"]+"@"+config.credentials["host"]+":"+config.credentials["port"]+"/"+config.credentials["database"]
engine = create_engine(DB_CONNECT_STRING)
connection = engine.connect()



models_cal = Blueprint('models_cal', __name__ )
@models_cal.route("/api/models/cal", methods=["POST"])
def cal_call():

	try:
		test_json = request.get_json()
	except Exception as e:
		raise e


	try:
		json_gender = int(test_json["gender"])
		json_age = int(test_json["age"])
		json_arrival_2 = int(test_json["arrival_2"])
		json_ecode_type = int(test_json["ecode_type"])
	except Exception as e:
		return(bad_request())




	def get_iss_ratio(gender, age, arrival_2, ecode_type):

		cur = connection.execute(
			'SELECT ISS FROM d4sg_trauma_03 WHERE gender={} and age<{} and age>{} and arrival_way_2={} and ecode_type={}'
			.format(gender, age+3, age-3, arrival_2, ecode_type)) 

		d = pd.DataFrame(list(cur))


		return (len(d[d[0]>16])/len(d))


	def get_OHCA_ratio(gender, age, arrival_2, ecode_type):

		cur = connection.execute(
			'SELECT OHCA FROM d4sg_trauma_03 WHERE gender={} and age<{} and age>{} and arrival_way_2={} and ecode_type={}'
			.format(gender, age+3, age-3, arrival_2, ecode_type)) 

		d = pd.DataFrame(list(cur))


		return (len(d[d[0]==1])/len(d))



	def get_los_mean(gender, age, arrival_2, ecode_type):

		cur = connection.execute(
			'SELECT los FROM d4sg_trauma_03 WHERE gender={} and age<{} and age>{} and arrival_way_2={} and ecode_type={}'
			.format(gender, age+3, age-3, arrival_2, ecode_type)) 

		d = pd.DataFrame(list(cur))


		return d[0].mean()

	def get_survival_rate(gender, age, arrival_2, ecode_type):

		cur = connection.execute(
			'SELECT outcome_3 FROM d4sg_trauma_03 WHERE gender={} and age<{} and age>{} and arrival_way_2={} and ecode_type={}'
			.format(gender, age+3, age-3, arrival_2, ecode_type)) 

		d = pd.DataFrame(list(cur))


		return (len(d[d[0]==0])/len(d))
		
		



	payload = {
		"iss_ratio": "{:.0%}".format(round(get_iss_ratio(json_gender,json_age,json_arrival_2,json_ecode_type),2)),
		"OHCA_ratio": "{:.0%}".format(round(get_OHCA_ratio(json_gender,json_age,json_arrival_2,json_ecode_type),2)),
		"los_mean": int(round(get_los_mean(json_gender,json_age,json_arrival_2,json_ecode_type),0)),
		"los_points" : 18033*int(round(get_los_mean(json_gender,json_age,json_arrival_2,json_ecode_type),0)),
		"los_burden_cost" : 711*int(round(get_los_mean(json_gender,json_age,json_arrival_2,json_ecode_type),0)),
		"survival_rate": "{:.0%}".format(round(get_survival_rate(json_gender,json_age,json_arrival_2,json_ecode_type),2))
	}

	responses = jsonify(payload)
	responses.status_code = 200


	
	return (responses)




# @app.errorhandler(400)
# def bad_request(error=None):
# 	message = {
# 			'status': 400,
# 			'message': 'Bad Request: ' + request.url + '--> Please check your data payload...',
# 	}
# 	resp = jsonify(message)
# 	resp.status_code = 400

# 	return responses



if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)









