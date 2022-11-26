"""
moduletest.py contains functions for test case.
"""
"""
1= valid data

0= not valid data
"""


def check_valid_data_temperature(number):
        if(-40<=number['temperature']<=85.0):
            return 1
        else:
            return 0

def check_valid_data_humidity(number):
        if(0.0<=number['humidity']<=100.0):
            return 1
        else:
            return 0

def check_valid_data_lux(number):
        if(0.0<=number['lux']<=65535.0):
            return 1
        else:
            return 0  

def check_valid_data_lw(number):
        if(0.0<=number['lw']<=1.0):
            return 1
        else:
            return 0        
    
    
def check_valid_data_pressure(number):
        if(300.0<=number['pressure']<=1100.0):
            return 1
        else:
            return 0  

   
    
def check_valid_data_rainfall(number):
        if(0.0<=number['rainfall']<=100.0):
            return 1
        else:
            return 0

def check_valid_data_soil_moisture(number):
        if(0.0<=number['soil_moisture']<=200.0):
            return 1
        else:
            return 0 

def check_valid_data_windspeed(number):
        if(0.0<=number['windspeed']):
            return 1
        else:
            return 0


        