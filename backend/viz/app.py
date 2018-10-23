
from flask import Flask, jsonify, Blueprint
import pandas as pd
import json
from sqlalchemy import create_engine
from flask_cors import CORS
import config



app = Flask(__name__)
CORS(app)

DB_CONNECT_STRING = "mysql+pymysql://" + config.credentials["username"]+ ":"+config.credentials["password"]+"@"+config.credentials["host"]+":"+config.credentials["port"]+"/"+config.credentials["database"]
engine = create_engine(DB_CONNECT_STRING)
connection = engine.connect()


viz_d1 = Blueprint('viz_d1', __name__ )
@viz_d1.route("/api/viz/d1", methods=["GET"])
def get_task_d1():
    d1 = pd.read_csv("viz/data/data_1a.csv")
    d1.sort_values(["合計"],ascending=False,inplace=True)

    js1 = {
        "x":list(d1["合計"]),
        "y":list(d1["X"])
    }

    return json.dumps(js1)



viz_d2 = Blueprint('viz_d2', __name__ )
@viz_d2.route("/api/viz/d2", methods=["GET"])
def get_task_d2():
    d2 = pd.read_csv("viz/data/data_4a.csv")
    d2.sort_values(["V2"],ascending=False,inplace=True)

    js2 = {
    "x":list(d2["V2"]),
    "y":list(d2["V1"])
    }

    return json.dumps(js2)




# -- 
viz_d3 = Blueprint('viz_d3', __name__ )
@viz_d3.route("/api/viz/d3", methods=["GET"])
def get_task_d3():

    cur = connection.execute('SELECT age,ecode_type FROM d4sg_trauma_03') 

    d = pd.DataFrame(list(cur.cursor))
    d.columns = ["age","ecode_type"]

    x = list(range(120))
    list_df = []
    for i in range(1,13,1):
        df = d.groupby("ecode_type").get_group(i)
        count = pd.DataFrame(df["age"].value_counts())
        count.reset_index(inplace=True)
        count.columns = ["age", "count_"]
    
        list_age = []
        list_count = []
        for a in x:
            if a not in list(count["age"]):
                list_age.append(a)
                list_count.append(0)
            
        new = pd.DataFrame()
        new["age"] = list(count["age"])+list_age
        new["count_{}".format(i)] = list(count["count_"])+list_count
        new.sort_values("age",inplace=True)
        new.reset_index(drop=True,inplace=True)

        #new["count_{}".format(i)] = new["count_{}".format(i)]/new["count_{}".format(i)].sum()

    
        del new["age"]
    
        list_df.append(new)

    final = pd.concat(list_df, axis=1)

    js3 = dict()
    js3["x"] = x
    for i in range(1,13):
        col_name = "count_{}".format(i)
        js3["y{}".format(i)] = list(final[col_name])

    return json.dumps(js3)


    





viz_d4 = Blueprint('viz_d4', __name__ )
@viz_d4.route("/api/viz/d4", methods=["GET"])
def get_task_d4():




    cur = connection.execute('SELECT age FROM d4sg_trauma_03 WHERE gender=2 and ecode_type=1') # gender=2, female
    d_female = pd.DataFrame(list(cur.cursor))
    d_female = pd.DataFrame(d_female[0].value_counts())
    d_female = d_female.reset_index()
    d_female.sort_values(["index"],inplace=True)

    cur = connection.execute('SELECT age FROM d4sg_trauma_03 WHERE gender=1 and ecode_type=1') # gender=1, male
    d_male = pd.DataFrame(list(cur.cursor))
    d_male = pd.DataFrame(d_male[0].value_counts())
    d_male = d_male.reset_index()
    d_male.sort_values(["index"],inplace=True)


    js4 = {

    "x_female":list(d_female[0]),
    "y_female":list(d_female["index"]),

    "x_male":list(d_male[0]*(-1)),
    "y_male":list(d_male["index"])

    }





    return json.dumps(js4)



viz_d5 = Blueprint('viz_d5', __name__ )
@viz_d5.route("/api/viz/d5", methods=["GET"])
def get_task_d5():


    

    cur = connection.execute('SELECT age FROM d4sg_trauma_03 WHERE gender=2 and ecode_type=2') # gender=2, female
    d_female = pd.DataFrame(list(cur.cursor))
    d_female = pd.DataFrame(d_female[0].value_counts())
    d_female = d_female.reset_index()
    d_female.sort_values(["index"],inplace=True)

    cur = connection.execute('SELECT age FROM d4sg_trauma_03 WHERE gender=1 and ecode_type=2') # gender=1, male
    d_male = pd.DataFrame(list(cur.cursor))
    d_male = pd.DataFrame(d_male[0].value_counts())
    d_male = d_male.reset_index()
    d_male.sort_values(["index"],inplace=True)


    js5 = {

    "x_female":list(d_female[0]),
    "y_female":list(d_female["index"]),

    "x_male":list(d_male[0]*(-1)),
    "y_male":list(d_male["index"])

    }





    return json.dumps(js5)



viz_d6 = Blueprint('viz_d6', __name__ )
@viz_d6.route("/api/viz/d6", methods=["GET"])
def get_task_d6():
    d6 = pd.read_csv("viz/data/rpub_6.csv")
    d6.sort_values(["V2"],ascending=False,inplace=True)

    js6 = {
    "x":list(d6["V2"]),
    "y":list(d6["V1"])
    }

    return json.dumps(js6)


viz_d7 = Blueprint('viz_d7', __name__ )
@viz_d7.route("/api/viz/d7", methods=["GET"])
def get_task_d7():
    d7 = pd.read_csv("viz/data/rpub_7.csv")
    d7.sort_values(["V2"],ascending=False,inplace=True)

    js7 = {
    "x":list(d7["V2"]),
    "y":list(d7["V1"])
    }

    return json.dumps(js7)








if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

