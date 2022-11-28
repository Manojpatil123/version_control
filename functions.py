import pandas as pd
from datetime import date
import warnings
warnings.filterwarnings('ignore')
from jira import JIRA
from tabulate import tabulate
import duckdb
import smtplib
from email.message import EmailMessage 
import mysql.connector


class sensortracking:

    def sql_connection(imei_no,DB_PASSWORD):
        conn_object=mysql.connector.connect(host="ls-25680f515e471efdf54796f570a95d35d48c083c.crx199snke8e.ap-south-1.rds.amazonaws.com",  user="outgrow",  password="{0}".format(str(DB_PASSWORD)), database='dbmaster')
        cur_object=conn_object.cursor()                                                                                                                                              
        query="select * from gwx_raw_iot_data where  imei_no = '{0}' ".format(str(imei_no))
        #excecute cursor
        cur_object.execute(query)
        #display records
        table=cur_object.fetchall()
        return table



    #send mail if error occurs
    def send_mail(MAIL_PASSWORD):
        sender_email = "manoj.mruthyunjayappa@waycool.in"         
      
        password="{0}".format(str(MAIL_PASSWORD))      #app password      
        rec_email=['manoj.mruthyunjayappa@waycool.in','sandeep.srinivas@waycool.in']
        message = EmailMessage()
        message['From']=sender_email
        message['To']=", ".join(rec_email)
        message['Subject']='Sensor tracking logs report {} .'.format(date.today())
        message.set_content('Hi team \nThis is the logs report of sensor tracking project')
        with open('logs.txt', 'rb') as f:  
            file_data = f.read()
            file_name = f.name    
        message.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
        server=smtplib.SMTP('smtp.gmail.com',587) 
        server.starttls()
        server.login(sender_email,password)
        server.send_message(message)
        server.quit()


    #rise jira ticket if issue present in data 
    def jira_ticket(sensor_issues_report,dates,id,JIRA_API):
        jira=JIRA(basic_auth=('noreplyit@waycool.in', '{0}'.format(str(JIRA_API))  ),server="https://censanext.atlassian.net")
                    
        issue_dict = {
            'project': {'key':'OFIT'},  
            'summary': 'IOT Device sensor issues for the date interval from {0} to {1}'.format(dates[-1],dates[0]),
            'description':tabulate(sensor_issues_report, tablefmt='jira',headers=sensor_issues_report.columns),
            "issuetype": {"name": "Task"},       
            'assignee' : { 'id' : id},
            
        }
        
        sensor_issues_report.to_csv('report.csv')

        key_value=jira.create_issue(fields=issue_dict)#key of issue created 
        issue=jira.issue(key_value.key)
        jira.add_attachment(issue=issue, attachment='report.csv')

    #count of data of each column
    def count_of_valid_data(a):

        a['temperature']=  duckdb.query("select count(*) from orginal_df where temperature <= 85.0 and temperature >=-40.0").df().iloc[0,0]
        a['humidity']=  duckdb.query('select count(*) from orginal_df where humidity >= 0.0 and humidity <=100.0').df().iloc[0,0]
        a['lux']=  duckdb.query('select count(*) from orginal_df where lux >= 0.0 and lux <=65535.0').df().iloc[0,0]
        a['lw']=  duckdb.query('select count(*) from orginal_df where lw > 0.0 and lw <=100.0').df().iloc[0,0]
        a['pressure']=  duckdb.query('select count(*) from orginal_df where pressure >= 300.0 and pressure <=1100.0').df().iloc[0,0]
        a['rainfall']=duckdb.query('select count(*) from orginal_df where rainfall >= 0.0 and rainfall <=100.0').df().iloc[0,0]
        a['soil_moisture1']=duckdb.query('select count(*) from orginal_df where soil_moisture1 >= 0.0 and soil_moisture1 <=100.0').df().iloc[0,0]
        a['soil_moisture2']=duckdb.query('select count(*) from orginal_df where soil_moisture2 >= 0.0 and soil_moisture2 <=100.0').df().iloc[0,0]
        a['soil_temperature']=duckdb.query('select count(*) from orginal_df where soil_temperature >= -55.0 and soil_temperature <=125.0').df().iloc[0,0]
        a['windspeed']=duckdb.query('select count(*) from orginal_df where windspeed > 0.0' ).df().iloc[0,0]
        a['winddirection']=duckdb.query('select count(*) from orginal_df where winddirection >= 0.0').df().iloc[0,0]
        return a

    #checking sensor issues
    def list_of_sensor_have_issues( issues_list,str1,orginal_df,dates,a):
    
        columns_name=['temperature','humidity','lux','lw','pressure','rainfall','soil_moisture1','soil_moisture2','soil_temperature','windspeed','winddirection']
        percentage=0.0
        for ele in columns_name:
            if(a[ele]!=orginal_df[ele].shape[0] ):#checking count of valid data equal to total value or not
                if(ele=='windspeed'): #checking not valid windspeed data for a day         
                    for m in dates:
                      b=pd.DataFrame()
                      orginal_df1=orginal_df[orginal_df['date']==m]
                      b=orginal_df1[(orginal_df1['windspeed'] <= 0.0)]#for each day checking not valid data 
                      percentage=b['windspeed'].value_counts().sum()/orginal_df1.shape[0]*100 #checking ratio of not valid data to total count of data                     
                      if(percentage==100.0):# if ratio is 100 consider windspeed sensor has issue
                        str1+=ele
                        break
                
                        
                elif(ele=='soil_moisture1'):
                    for m in dates:
                      b=pd.DataFrame()
                      orginal_df1=orginal_df[orginal_df['date']==m]
                      b=orginal_df1[(orginal_df1['soil_moisture1'] == 200)]#for each day checking not valid data 
                      percentage=b['soil_moisture1'].value_counts().sum()/orginal_df1.shape[0]*100 #checking ratio of not valid data to total count of data                     
                      if(percentage==100.0):# if ratio is 100 consider windspeed sensor has issue
                        str1+=ele+','
                        break
                
                elif(ele=='soil_moisture2'):
                    for m in dates:
                      b=pd.DataFrame()
                      orginal_df1=orginal_df[orginal_df['date']==m]
                      b=orginal_df1[(orginal_df1['soil_moisture2'] == 200.0)]#for each day checking not valid data 
                      percentage=b['soil_moisture2'].value_counts().sum()/orginal_df1.shape[0]*100 #checking ratio of not valid data to total count of data                     
                      if(percentage==100.0):# if ratio is 100 consider windspeed sensor has issue
                        str1+=ele+","
                        break

                elif(ele=='lw'):
                    b=pd.DataFrame()
                    orginal_df1=orginal_df[(orginal_df['date']==dates[0]) | (orginal_df['date']==dates[1]) ]
                    b=orginal_df1[(orginal_df1['lw'] == 0)]#for each day checking not valid data 
                    percentage=b['lw'].value_counts().sum()/orginal_df1.shape[0]*100 #checking ratio of not valid data to total count of data                     
                    if(percentage==100.0):# if ratio is 100 consider windspeed sensor has issue
                       str1+=ele+','

                else:
                    str1+=ele+','
        if(len(str1)>1):
            issues_list.append(str1)  # type: ignore
            return issues_list
        else:
                issues_list.append('no issues')
                return issues_list


    #sample not valid data
    def sample_data_of_not_valid_sensor(orginal_df,not_valid_data,issues_list):
        b=pd.DataFrame()
        b=orginal_df[( orginal_df['temperature'] >85.0) | ( orginal_df['temperature'] <-40.0)]
        if(b['temperature'].shape[0]!=0):
            not_valid_data['temperature']=set(b['temperature'].sort_values(ascending=False)[0:10].values)

        b=pd.DataFrame()
        b=orginal_df[(orginal_df['humidity']<0.0) | (orginal_df['humidity'] > 100.0)]
        if(b['humidity'].shape[0]!=0):
            not_valid_data['humidity']=set(b['humidity'].sort_values(ascending=False)[0:10].values)

        b=pd.DataFrame()
        b=orginal_df[(orginal_df['lux']<0.0) | (orginal_df['lux'] > 65535.0)]
        if(b['lux'].shape[0]!=0):
            not_valid_data['lux']=set(b['lux'].sort_values(ascending=False)[0:10].values)


        b=pd.DataFrame()
        b=orginal_df[(orginal_df['pressure']< 300.0) | (orginal_df['pressure'] > 1100.0)]  # type: ignore
        if(b['pressure'].shape[0]!=0):
            not_valid_data['pressure']=set(b['pressure'].sort_values(ascending=False)[0:10].values)

        b=pd.DataFrame()
        b=orginal_df[(orginal_df['rainfall'] <0.0) | (orginal_df['rainfall'] > 100.0)]
        if(b['rainfall'].shape[0]!=0):
            not_valid_data['rainfall']=set(b['rainfall'].sort_values(ascending=False)[0:10].values)

            
        b=pd.DataFrame()
        b=orginal_df[(orginal_df['soil_temperature'] < -55.0) | (orginal_df['soil_temperature'] > 125.0)]
        if(b['soil_temperature'].shape[0]!=0):      
            not_valid_data['soil_temperature']=set(b['soil_temperature'].sort_values(ascending=False)[0:10].values)
        
        if('lw' in issues_list[-1]):
                b=pd.DataFrame()
                b=orginal_df[(orginal_df['lw'] == 0)]
                if(b['lw'].shape[0]!=0):                 
                    not_valid_data['lw']=set(b['lw'].sort_values(ascending=False)[0:3].values)
        
        if('soil_moisture1' in issues_list[-1]):
                b=pd.DataFrame()
                b=orginal_df[(orginal_df['soil_moisture1'] == 200)]
                if(b['soil_moisture2'].shape[0]!=0):                 
                    not_valid_data['soil_moisture1']=set(b['soil_moisture1'].sort_values(ascending=False)[0:3].values)

        if('soil_moisture2' in issues_list[-1]):
                b=pd.DataFrame()
                b=orginal_df[(orginal_df['soil_moisture2'] == 200)]
                if(b['soil_moisture2'].shape[0]!=0):                 
                    not_valid_data['soil_moisture2']=set(b['soil_moisture2'].sort_values(ascending=False)[0:3].values)


        if('windspeed' in issues_list[-1]):
                b=pd.DataFrame()
                b=orginal_df[(orginal_df['windspeed'] <= 0.0)]
                if(b['windspeed'].shape[0]!=0):                 
                    not_valid_data['windspeed']=set(b['windspeed'].sort_values(ascending=False)[0:3].values)

        sensor_issue={}
        for keys, values1 in not_valid_data.items():
                sensor_issue_value=[]
                for val in values1:
                    if(val==123456789.0):
                        val='None'
                        sensor_issue_value.append(val)
                    else:
                        sensor_issue_value.append(val)  
                sensor_issue[keys]=sensor_issue_value
        if(len(sensor_issue)>0):
            issues_list.append(sensor_issue)
            return issues_list
        else:
            issues_list.append(0)
            return issues_list

    #priority of issues
    def sensor_issues_priority_level(dates,orginal_df,orginal_df1,issues_list, priority_of_issues):
        priority_of_issues.append(duckdb.query('select  round(count(temperature)*100/(select count(*) from orginal_df1),1) as temp from (select * from orginal_df where temperature > 85.0 or temperature <-40.0)').df().iloc[0,0])
        priority_of_issues.append(duckdb.query('select  round(count(lux)*100/(select count(*) from orginal_df1),1) as lux from (select * from orginal_df where lux < 0.0 or lux >65535.0)').df().iloc[0,0])
        priority_of_issues.append(duckdb.query('select  round(count(humidity)*100/(select count(*) from orginal_df1),1)as humidity from( select * from orginal_df where humidity < 0.0 or humidity >100.0)').df().iloc[0,0])
        priority_of_issues.append(duckdb.query('select  round(count(pressure)*100/(select count(*) from orginal_df1),1) as pressure from( select * from orginal_df where pressure < 300.0 or pressure > 1100.0)').df().iloc[0,0])
        priority_of_issues.append(duckdb.query('select  round(count(rainfall)*100/(select count(*) from orginal_df1),1) as rainfall from( select * from orginal_df where rainfall < 0.0 or rainfall > 100.0)').df().iloc[0,0])
        priority_of_issues.append(duckdb.query('select  round(count(winddirection)*100/(select count(*) from orginal_df1),1) as winddirection from( select * from orginal_df where winddirection < 0.0)').df().iloc[0,0])
        priority_of_issues.append(duckdb.query('select round(count(soil_temperature)*100/(select count(*) from orginal_df1),1) as soil_temperature from (select * from orginal_df where soil_temperature < -55.0 or soil_temperature >125.0)').df().iloc[0,0])
        
        percentage=0.0
        b=pd.DataFrame()
        orginal_df1=orginal_df[(orginal_df['date']==dates[0]) | (orginal_df['date']==dates[1]) ]
        b=orginal_df1[(orginal_df1['lw'] == 0)]
        if(b['lw'].shape[0]!=0):                 
            percentage=b['lw'].value_counts().sum()/orginal_df1.shape[0]*100
        if(str(percentage)==str(100.0)):
            priority_of_issues.append(percentage)
        
        for m in dates:
                b=pd.DataFrame()
                orginal_df1=orginal_df[orginal_df['date']==m]
                b=orginal_df1[(orginal_df1['soil_moisture1'] == 200.0)]
                if(b['soil_moisture1'].shape[0]!=0):                 
                    percentage=b['soil_moisture1'].value_counts().sum()/orginal_df1.shape[0]*100
                if(str(percentage)==str(100.0)):
                    priority_of_issues.append(percentage)
        
        for m in dates:
                b=pd.DataFrame()
                orginal_df1=orginal_df[orginal_df['date']==m]
                b=orginal_df1[(orginal_df1['soil_moisture2'] == 200.0 )]
                if(b['soil_moisture2'].shape[0]!=0):                 
                    percentage=b['soil_moisture2'].value_counts().sum()/orginal_df1.shape[0]*100
                if(str(percentage)==str(100.0)):
                    priority_of_issues.append(percentage)



        for m in dates:
                b=pd.DataFrame()
                orginal_df1=orginal_df[orginal_df['date']==m]
                b=orginal_df1[(orginal_df1['windspeed'] <= 0.0)]
                if(b['windspeed'].shape[0]!=0):                 
                    percentage=b['windspeed'].value_counts().sum()/orginal_df1.shape[0]*100
                if(str(percentage)==str(100.0)):
                    priority_of_issues.append(percentage)
        priority_of_issues.sort(reverse=True)
        
        if(len(priority_of_issues)>0):
            if(priority_of_issues[0]>=30.0):
                    issues_list.append("Critical priority")
                    return issues_list
            elif(priority_of_issues[0]>=20.0 and priority_of_issues[0]<29.0):
                    issues_list.append("High Priority")
                    return issues_list
            elif(priority_of_issues[0]>=10.0 and priority_of_issues[0]<19.0):
                    issues_list.append("Medium Priority")
                    return issues_list
            else:
                    issues_list.append('Low priority')
                    return issues_list
        else:
                issues_list.append('no issues')
                return issues_list

    #sensor issues dates
    def sensor_issues_occured_date(sensor_issues_dates,dates,orginal_df,issues_list):
        sensor_issues_dates['temperature']=list(duckdb.query('select distinct(date) from  (select * from orginal_df where temperature >85.0 or temperature <-40.0 )').df().iloc[0:,0])
        sensor_issues_dates['humidity']=list(duckdb.query('select distinct(date) from  (select * from orginal_df where humidity < 0.0 or humidity >100.0)').df().iloc[0:,0])
        sensor_issues_dates['lux']=list(duckdb.query('select distinct(date) from  (select * from orginal_df where lux < 0.0 or lux >65535.0 )').df().iloc[0:,0])
        sensor_issues_dates['pressure']=list(duckdb.query('select distinct(date) from  ( select * from orginal_df where pressure < 300.0 or pressure > 1100.0 )').df().iloc[0:,0])
        sensor_issues_dates['rainfall']=list(duckdb.query('select distinct(date) from  (select * from orginal_df where rainfall < 0.0 or rainfall > 100.0 )').df().iloc[0:,0])
        sensor_issues_dates['winddirection']=list(duckdb.query('select distinct(date) from  (select * from orginal_df where winddirection < 0.0)').df().iloc[0:,0])
        sensor_issues_dates['soil_temperature']=list(duckdb.query('select distinct(date) from (select * from orginal_df where soil_temperature < -55.0 or soil_temperature >125.0)').df().iloc[0:,0])
        
        percentage=0.0
        dates_value=[]
        b=pd.DataFrame()
        orginal_df1=orginal_df[(orginal_df['date']==dates[0]) | (orginal_df['date']==dates[1])]
        b=orginal_df1[(orginal_df1['lw'] == 0)]
        if(b['lw'].shape[0]!=0):    
            percentage=b['lw'].value_counts().sum()/orginal_df1.shape[0]*100
        if(str(percentage)==str(100.0)):          
            set2=set(b['date'])
            for k in set2:
                dates_value.append(str(k))
        if(len(dates_value)!=0):
                sensor_issues_dates['lw']=dates_value
        
        dates_value=[]
        for m in dates:
                b=pd.DataFrame()
                orginal_df1=orginal_df[orginal_df['date']==m]
                b=orginal_df1[(orginal_df1['soil_moisture1'] == 200.0)]
                if(b['soil_moisture1'].shape[0]!=0):    
                    percentage=b['soil_moisture1'].value_counts().sum()/orginal_df1.shape[0]*100
                if(str(percentage)==str(100.0)):          
                    set2=set(b['date'])
                    for k in set2:
                      dates_value.append(str(k))
        if(len(dates_value)!=0):
                sensor_issues_dates['soil_moisture1']=dates_value

        dates_value=[]
        for m in dates:
                b=pd.DataFrame()
                orginal_df1=orginal_df[orginal_df['date']==m]
                b=orginal_df1[(orginal_df1['soil_moisture2'] == 200.0)]
                if(b['soil_moisture2'].shape[0]!=0):    
                    percentage=b['soil_moisture2'].value_counts().sum()/orginal_df1.shape[0]*100
                if(str(percentage)==str(100.0)):          
                    set2=set(b['date'])
                    for k in set2:
                      dates_value.append(str(k))
        if(len(dates_value)!=0):
                sensor_issues_dates['soil_moisture2']=dates_value
        

        dates_value=[]
        for m in dates:
                b=pd.DataFrame()
                orginal_df1=orginal_df[orginal_df['date']==m]
                b=orginal_df1[(orginal_df1['windspeed'] <= 0.0)]
                if(b['windspeed'].shape[0]!=0):    
                    percentage=b['windspeed'].value_counts().sum()/orginal_df1.shape[0]*100
                if(str(percentage)==str(100.0)):          
                    set2=set(b['date'])
                    for k in set2:
                       dates_value.append(str(k))
        if(len(dates_value)!=0):
                sensor_issues_dates['windspeed']=dates_value


        #converting timestamp to date 
        for key,value in sensor_issues_dates.items():
                value1=[]
                for val in value:
                    value1.append(str(val))
                sensor_issues_dates[key] = value1
                
        if(len(sensor_issues_dates)>0):
            issue_date={}
            for key,values in sensor_issues_dates.items():
                if(len(values)!=0) :
                    issue_date[key]=list(values)     
            issues_list.append(issue_date)
            return issues_list
        else:
                issues_list.append(0)
                return issues_list


    #sensor not sent data dates
    def hours_which_no_data(list_of_hours,dates,orginal_df,issues_list):
        orginal_df['hour']=pd.to_datetime(orginal_df.timestamp).dt.hour
        
        for m in dates:
            list_hour=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
            orginal_df1=orginal_df[(orginal_df['date']==m)]
            hours_list=set(orginal_df1['hour'].values)
            for n in list_hour:
                if(n not in hours_list):
                    hour=str(m) +' '+ str(n)
                    list_of_hours.append(hour)
        
        if(len(list_of_hours)>0):
            issues_list.append(list_of_hours)
            return issues_list
        else:
            issues_list.append('Network_connection_is_good')
            return issues_list
        
