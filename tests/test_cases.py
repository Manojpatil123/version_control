import pytest
from tests.moduletest import check_valid_data_soil_moisture, check_valid_data_windspeed
from tests.moduletest import check_valid_data_temperature, check_valid_data_humidity,check_valid_data_lux
from tests.moduletest import check_valid_data_lw, check_valid_data_rainfall,check_valid_data_pressure 

@pytest.fixture
def input():
   number={}
   number['temperature'] = 35.0
   number['humidity']=85.0
   number['lux']= 1289.0
   number['lw']=0.0
   number['pressure']=1950.0
   number['rainfall']=55.5
   number['soil_moisture']=26.0
   number['windspeed']=-5.0

   return number

class Test:
    def test_temperature(input):
        number=input()
        Temperature=check_valid_data_temperature(number)
        assert Temperature == 1

    def test_humidity(input):
        number=input()
        humidity=check_valid_data_humidity(number)
        assert humidity == 1

    def test_lux(input):
        number=input()
        lux=check_valid_data_lux(number)
        assert lux == 1

    def test_lw(input):
        number=input()
        lw=check_valid_data_lw(number)
        assert lw == 1

    def test_pressure(input):
        number=input()
        pressure=check_valid_data_pressure(number)
        assert pressure == 0

    def test_rainfall(input):
        number=input()
        rainfall=check_valid_data_rainfall(number)
        assert rainfall == 1
        
        
    def test_soil_moisture(input):
        number=input()
        soil_moisture=check_valid_data_soil_moisture(number)
        assert soil_moisture == 1

    def test_windspeed(input):
        number=input()
        windspeed=check_valid_data_windspeed(number)
        assert windspeed == 0
        
