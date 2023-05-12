from flask import Flask, render_template, request
import requests
import json
import pandas as pd
from datetime import datetime
import numpy as np

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('home.html')

url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
d = requests.get(url).json()
global token_df
token_df = pd.DataFrame.from_dict(d)
token_df['expiry'] = pd.to_datetime(token_df['expiry'])
token_df = token_df.astype({'strike': float})


@app.route('/token',methods=['GET', 'POST'])
def token():
    if request.method == 'POST':
      exch_seg=request.form['exch_seg']
      instrumenttype=request.form['instrumenttype']
      symbol=request.form['symbol']
      strike_price=request.form['strike_price']
      pe_ce=request.form['pe_ce']
    
    strike_price=int(strike_price)
    df = token_df
    strike_price = strike_price*100
    eq_df = df[(df['exch_seg'] == exch_seg) & (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol) & (df['strike'] == strike_price) &(df['symbol'].str.endswith(pe_ce))]


    return render_template('token.html',tables=[eq_df.to_html(classes='data')], header="true" )


print(__name__)
if __name__ == "__main__":
  app.run(host='0.0.0.0',debug=True)