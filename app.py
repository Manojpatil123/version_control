
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
def version():
    try:
        version = open('version', 'r').read()
    except:
        version = 'v0.0.0'
    return jsonify({"version": version})

    

@app.route('/result')
def report1():
   sensor_issues_report=pd.DataFrame(columns=['Buyer','Imei','device','location','Active','sensor_issues',"sensor_issue_data","issue_priority",'dates_of_faulty_data','hours_which_no_data'])
   try: 
      dataframe=pd.read_csv('https://docs.google.com/spreadsheets/d/1-RGaGIa5RpFjCdyu2HiIFpTEvzBjLeIlXCk8N5KXfWQ/export?format=csv')
 
      #for i in range(0,len(dataframe)):
      for i in range(0,len(dataframe)):
        try:  
              
         imei_no=str(dataframe.iloc[i,0])#getting imei from sheet        
         df=sensortracking.sql_connection(imei_no,DB_PASSWORD)
         df1=pd.DataFrame(df,columns=['id','timestamp','imei_no','temperature','pressure','humidity','rainfall','windspeed','winddirection','soil_moisture1','soil_moisture2','lw','soil_temperature','lux','flow_meter','raw_data','created_at','updated_at'])
         if(len(df)>0):
                print('connection')
         if(df1.shape[0]==0):#checking values are there or not in dataframe      
            pass
         else:
            df1['date']=pd.to_datetime(df1.timestamp).dt.date#converting timestamp to date format                  
            columns_name=['temperature','humidity','lux','lw','pressure','rainfall','soil_moisture1','soil_moisture2','soil_temperature','windspeed','winddirection']
            for ele in columns_name:  
               df1[ele].replace('None',123456789.0,inplace=True)
               df1[ele].replace(np.nan,123456789.0,inplace=True)      
               if 123456789.0 in df1[ele].values:#if none present in sensor replacing with 123456789.0 value
                  #df1[ele].replace(np.nan,123456789.0,inplace=True)
                  df1[ele]=df1[ele].astype(float)
               else:
                  df1[ele]=df1[ele].astype(float)#converting to float

            #getting  continuous 2 days data
            dates=[]
            dates.append(date.fromordinal(date.today().toordinal()-1))
            dates.append(date.fromordinal(date.today().toordinal()-2))
        
            #getting  continuous 2 days data
            orginal_df=pd.DataFrame()
            orginal_df=df1[(df1['date']==date.fromordinal(date.today().toordinal()-1)) | (df1['date']==date.fromordinal(date.today().toordinal()-2)) ]
            orginal_df1=orginal_df

            if(orginal_df.shape[0]==0):#checking orginal_df has data or not if data not there return none
               pass             
            else:
           #adding count of values of each column
               a={}
               sensortracking.count_of_valid_data(a)

            #report generation
               issues_list=[]             
               str1=" "
               issues_list.append(str(dataframe.iloc[i,3]))#getting buyer name from sheet
               issues_list.append(dataframe.iloc[i,0])#getting imei no from sheet
               issues_list.append(str(dataframe.iloc[i,1]))#getting device name from sheet
               issues_list.append(str(dataframe.iloc[i,2]))#getting location name from sheet
               issues_list.append(str(dataframe.iloc[i,4]))#getting active status
               #storing 2 days dates in list for wind speed calculation
               
               # checking sensor issues
               sensortracking.list_of_sensor_have_issues( issues_list,str1,orginal_df,dates,a)
               
               #sample_data_of_not_valid
               not_valid_data={}  
               sensortracking.sample_data_of_not_valid_sensor(orginal_df,not_valid_data,issues_list)
               
              
              #priority of issues 
               priority_of_issues=[]   
               sensortracking.sensor_issues_priority_level(dates,orginal_df,orginal_df1,issues_list, priority_of_issues)
               
     
               #sensor issue dates
               sensor_issues_dates={}    
               sensortracking.sensor_issues_occured_date(sensor_issues_dates,dates,orginal_df,issues_list)

              #sensor not sent data dates
               list_of_hours=[]
               sensortracking.hours_which_no_data(list_of_hours,dates,orginal_df,issues_list)
               
               #adding result to dataframe 
               if('no issues' not in issues_list):           
               
                 sensor_issues_report.loc[i]=issues_list  
                 sensor_issues_report.reset_index(inplace=True,drop=True)
                 print('jira')
                 
        except Exception as e:
          logging.error(e)
          continue
  
      if(sensor_issues_report.shape[0]!=0):
         #create jira ticket if issue in data 
        # sensortracking.jira_ticket(sensor_issues_report,dates,id,JIRA_API)
        print('jira')
         
        
   except Exception as e:
         logging.error(e)
         #send logs mail if any error occur
         sensortracking.send_mail(MAIL_PASSWORD)
         

   result_dict=sensor_issues_report.to_dict(orient='records')
   return jsonify(result_dict)   

if __name__ == '__main__':
    app.run(port=80,debug=True)


     



     





