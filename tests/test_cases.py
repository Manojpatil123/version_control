import pytest
from moduletest import check_valid_data_soil_moisture, check_valid_data_windspeed
from moduletest import check_valid_data_temperature, check_valid_data_humidity,check_valid_data_lux
from moduletest import check_valid_data_lw, check_valid_data_rainfall,check_valid_data_pressure 

@pytest.fixture
def test_temperature():
    input={}
    input['temperature'] = 35.0
    input['humidity']=85.0
    input['lux']= 1289.0
    input['lw']=0.0
    input['pressure']=1950.0
    input['rainfall']=55.5
    input['soil_moisture']=26.0
    input['windspeed']=-5.0

    number=input
    Temperature=check_valid_data_temperature(number)
    assert Temperature == 1

def test_humidity():
    input={}
    input['temperature'] = 35.0
    input['humidity']=85.0
    input['lux']= 1289.0
    input['lw']=0.0
    input['pressure']=1950.0
    input['rainfall']=55.5
    input['soil_moisture']=26.0
    input['windspeed']=-5.0
    number=input
    humidity=check_valid_data_humidity(number)
    assert humidity == 1

def test_lux():
    input={}
    input['temperature'] = 35.0
    input['humidity']=85.0
    input['lux']= 1289.0
    input['lw']=0.0
    input['pressure']=1950.0
    input['rainfall']=55.5
    input['soil_moisture']=26.0
    input['windspeed']=-5.0
    number=input
    lux=check_valid_data_lux(number)
    assert lux == 1

def test_lw():
    input={}
    input['temperature'] = 35.0
    input['humidity']=85.0
    input['lux']= 1289.0
    input['lw']=0.0
    input['pressure']=1950.0
    input['rainfall']=55.5
    input['soil_moisture']=26.0
    input['windspeed']=-5.0
    number=input
    lw=check_valid_data_lw(number)
    assert lw == 1

def test_pressure():
    input={}
    input['temperature'] = 35.0
    input['humidity']=85.0
    input['lux']= 1289.0
    input['lw']=0.0
    input['pressure']=1950.0
    input['rainfall']=55.5
    input['soil_moisture']=26.0
    input['windspeed']=-5.0
    number=input
    pressure=check_valid_data_pressure(number)
    assert pressure == 0

def test_rainfall():
    input={}
    input['temperature'] = 35.0
    input['humidity']=85.0
    input['lux']= 1289.0
    input['lw']=0.0
    input['pressure']=1950.0
    input['rainfall']=55.5
    input['soil_moisture']=26.0
    input['windspeed']=-5.0
    number=input
    
    rainfall=check_valid_data_rainfall(number)
    assert rainfall == 1
    
    
def test_soil_moisture():
    input={}
    input['temperature'] = 35.0
    input['humidity']=85.0
    input['lux']= 1289.0
    input['lw']=0.0
    input['pressure']=1950.0
    input['rainfall']=55.5
    input['soil_moisture']=26.0
    input['windspeed']=-5.0
    
    number=input
    soil_moisture=check_valid_data_soil_moisture(number)
    assert soil_moisture == 1

def test_windspeed():
    input={}
    input['temperature'] = 35.0
    input['humidity']=85.0
    input['lux']= 1289.0
    input['lw']=0.0
    input['pressure']=1950.0
    input['rainfall']=55.5
    input['soil_moisture']=26.0
    input['windspeed']=-5.0
    
    number=input
    windspeed=check_valid_data_windspeed(number)
    assert windspeed == 0

