
from flask import Flask,jsonify
import pandas as pd
import numpy as np
from datetime import date
import warnings
warnings.filterwarnings('ignore')
import logging
from functions import sensortracking
import os




#getting all secrets
MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
DB_PASSWORD=os.environ.get('DB_PASSWORD')
JIRA_API=os.environ.get('JIRA_TOCKEN')



def report1():
   
      dataframe=pd.read_csv('https://docs.google.com/spreadsheets/d/1-RGaGIa5RpFjCdyu2HiIFpTEvzBjLeIlXCk8N5KXfWQ/export?format=csv')
 
      #for i in range(0,len(dataframe)):
      for i in range(0,len(dataframe)):
       
              
         imei_no=str(dataframe.iloc[i,0])#getting imei from sheet        
         df=sensortracking.sql_connection(imei_no,DB_PASSWORD)
         if(len(df)>0):
                print('connection')
                print(len(df))
         
      return len(df)

if __name__ == '__main__':
      report1()



     



     





