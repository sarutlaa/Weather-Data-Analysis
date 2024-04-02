import pytest
from flask_testing import TestCase
#importing the app.py created 
from app import app

class TestWeatherAPI(TestCase):
    '''
This function is designed to create test cases that examine and validate the query parameters.
It performs unit testing on specified parameter values to ensure they are correctly handled by the application.
    '''
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_weather_list_no_params(self):
        response = self.client.get('/api/weather/')
        self.assertEqual(response.status_code, 200)
        

    def test_weather_list_with_date(self):
        response = self.client.get('/api/weather/?date=1985-02-05')
        self.assertEqual(response.status_code, 200)
       

    def test_weather_list_with_station_id(self):
        response = self.client.get('/api/weather/?station_id=USC00130133')
        self.assertEqual(response.status_code, 200)
       
    def test_weather_stats_no_params(self):
        response = self.client.get('/api/weather/stats')
        self.assertEqual(response.status_code, 200)
       

    def test_weather_stats_with_year(self):
        response = self.client.get('/api/weather/stats?year=1985')
        self.assertEqual(response.status_code, 200)
        

    def test_weather_stats_with_station_id(self):
        response = self.client.get('/api/weather/stats?station_id=USC00130133')
        self.assertEqual(response.status_code, 200)
        
if __name__ == '__main__':
    pytest.main()
