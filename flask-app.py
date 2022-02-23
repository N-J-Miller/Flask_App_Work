#!usr/bin/env python

#pip install flask
from flask import Flask, json, render_template, request
import os
import numpy as np
import datetime


# Create instance of Flask app
app = Flask(__name__)

# decorator
@app.route("/")
def hello():
    return render_template('index.html', utc_dt=datetime.datetime.utcnow())

@app.route("/gdp")
def gdp():
    json_url = os.path.join(app.static_folder,"","us_gdp.json")
    data_json = json.load(open(json_url))

    return render_template('gdp_data.html',data=data_json)

@app.route("/gdp/<year>")
def gdp_year(year):
    json_url = os.path.join(app.static_folder,"","us_gdp.json")
    data_json = json.load(open(json_url))

    data = data_json[1]
    year = request.view_args['year']

    output_data = [x for x in data if x['date']==year]
    return render_template('gdp_data.html',data=output_data)

@app.route("/gdp/loop")
def gdp_loop():
    json_url = os.path.join(app.static_folder,"","us_gdp.json")
    data_json = json.load(open(json_url))

    data = data_json[1]
    data_dict = data[0]
    years = np.random.randint(low=1961, high=2021, size=10)
    GDP_Data = {'Year':[],'Country':[],
             'GDP in Dollars': []}

    for year in years:
        output_data = [x for x in data if x['date']==str(year)]
        output_dict = output_data[0]
        GDP_Data['Year'].append(output_dict['date'])
        GDP_Data['Country'].append(output_dict['country']['value'])
        GDP_Data['GDP in Dollars'].append(output_dict['value'])
                
        GDP_df = pd.DataFrame(GDP_Data)
        GDP_df = GDP_df.set_index(GDP_df.columns[0])

    return render_template('gdp_loop.html',data=GDP_df)

if __name__ == "__main__":
    app.run(debug=True)