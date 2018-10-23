import os
import pandas as pd
import pickle
from flask import Flask, jsonify, request, Blueprint
import random
from flask_cors import CORS


path = "models/iss/"


app = Flask(__name__)
CORS(app)



models_iss = Blueprint('models_iss', __name__ )
@models_iss.route("/api/models/iss", methods=["POST"])
def iss_call():
	try:
		test_json = request.get_json()
	except Exception as e:
		raise e
	
	def load_pickle(filename):
		with open(filename, 'rb') as handle:
			b = pickle.load(handle)
		return b



	def main_predict_fall(gener, age, arrival_1, OHCA, weekday):
	    clf = load_pickle(path+"0415_ISS_ageCon_fallRandomForest_clf")
	    enc = load_pickle(path+"0415_ISS_ageCon_Fall_encoder")
	    inputx2 = enc.transform([[gener, arrival_1, OHCA, weekday]]).toarray()
	    inputa =  list([age]) + list(inputx2[0])
	    return clf.predict([inputa])[0]

	def main_predict_car(gener, age, arrival_1, OHCA, weekday):
		clf = load_pickle(path+"0415_ISS_ageCon_car_clfRandomForest_clf")
		enc = load_pickle(path+"0415_ISS_ageCon_car_enc")
		inputx2 = enc.transform([[gener, arrival_1, OHCA, weekday]]).toarray()
		inputa =  list([age]) + list(inputx2[0])
		return clf.predict([inputa])[0]


	try:
		json_decision = test_json["ecode_type"]
		json_gender = int(test_json["gender"])
		json_age = int(test_json["age"])
		json_arrival_1 = int(test_json["arrival_1"])
		json_ohca = int(test_json["OHCA"])
		json_weekday = int(test_json["weekday"])
	except Exception as e:
		return(bad_request())



	def car_or_fall(decision):
		if decision == "fall":
			prediction = main_predict_fall(json_gender,json_age,json_arrival_1,json_ohca,json_weekday)
		elif decision =="car":
			prediction = main_predict_car(json_gender,json_age,json_arrival_1,json_ohca,json_weekday)

		# xd
		if prediction >= 0.98:
			prediction = prediction-random.uniform(0.05, 0.1)

		return prediction


	payload = {
		"prediction": "{:.0%}".format(round(car_or_fall(json_decision),2))
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









