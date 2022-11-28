
from flask import Flask,jsonify
import pandas as pd
import numpy as np
from datetime import date
import warnings
warnings.filterwarnings('ignore')
import logging
from functions import sensortracking
import os


app = Flask(__name__)
#creating logs file
logging.basicConfig(filename='logs.txt',filemode='a',format='%(asctime)s %(levelname)s=%(message)s',datefmt="%Y-%m-%d %H:%M:%S")
fi = open("logs.txt", "r+") 
# absolute file positioning
fi.seek(0) 
# to erase all data 
fi.truncate() 


#getting all secrets
MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
DB_PASSWORD=os.environ.get('DB_PASSWORD')
JIRA_API=os.environ.get('JIRA_TOCKEN')


@app.route('/')

def report1():
      sensor_issues_report=pd.DataFrame(columns=['Buyer','Imei','device','location','Active','sensor_issues',"sensor_issue_data","issue_priority",'dates_of_faulty_data','hours_which_no_data'])
   
      dataframe=pd.read_csv('https://docs.google.com/spreadsheets/d/1-RGaGIa5RpFjCdyu2HiIFpTEvzBjLeIlXCk8N5KXfWQ/export?format=csv')
 
      #for i in range(0,len(dataframe)):
      for i in range(0,len(dataframe)):
       
              
         imei_no=str(dataframe.iloc[i,0])#getting imei from sheet        
         df=sensortracking.sql_connection(imei_no,DB_PASSWORD)
         df1=pd.DataFrame(df,columns=['id','timestamp','imei_no','temperature','pressure','humidity','rainfall','windspeed','winddirection','soil_moisture1','soil_moisture2','lw','soil_temperature','lux','flow_meter','raw_data','created_at','updated_at'])
         if(len(df)>0):
                print('connection')
         
      return jsonify(len(df))

if __name__ == '__main__':
    app.run(port=80,debug=True)


     



     





