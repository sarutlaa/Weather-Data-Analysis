from flask import Flask, request
from flask_mysqldb import MySQL
from flask_restx import Api, Resource, fields
import logging

app = Flask(__name__)
api = Api(app, version='1.0', title='Weather API', description='A simple Weather API')

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Database configuration details, Please replace the host, user, password, database name accordingly.
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root@123'
app.config['MYSQL_DB'] = 'corteva'
mysql = MySQL(app)

ns = api.namespace('api/weather', description='Weather operations')

# Defining a model for weather data response
weather = api.model('Weather', {
    'id': fields.Integer(required=True, description='The weather record identifier'),
    'date': fields.String(required=True, description='The date of the record'),
    'max_temp': fields.Float(description='Maximum temperature'),
    'min_temp': fields.Float(description='Minimum temperature'),
    'precipitation': fields.Float(description='Precipitation'),
    'station_id': fields.String(description='Station ID')
})


# Defining a model for weather statistics response
statistics_model = api.model('WeatherStatistics', {
    'avg_max_temp': fields.Float(description='Average maximum temperature in degrees Celsius.'),
    'avg_min_temp': fields.Float(description='Average minimum temperature in degrees Celsius.'),
    'total_precipitation': fields.Float(description='Total accumulated precipitation in centimeters.')
})


@ns.route('/')
class WeatherList(Resource):
    """
    Class representing the API endpoint for retrieving a list of weather data records.

    Attributes:
        - None

    Methods:
        get(self): Retrieves a list of weather data records based on specified query parameters.
    """
    @ns.doc('list_weathers')
    @ns.expect(api.parser().add_argument('page', type=int, default=1, help='Page number')
               .add_argument('date', type=str, help='Filter by date')
               .add_argument('station_id', type=str, help='Filter by station ID'))
    @ns.marshal_list_with(weather)
    def get(self):
        """
        Retrieve a list of weather data records based on specified query parameters.

        Returns:
            List: A list of dictionaries representing weather data records.
        """
        parser = request.args
        page = parser.get('page', 1, type=int)
        date = parser.get('date', type=str)
        station_id = parser.get('station_id', type=str)

        query = "SELECT * FROM weather_data WHERE 1=1"
        query_params = []

        if date:
            query += " AND date = %s"
            query_params.append(date)

        if station_id:
            query += " AND station_id = %s"
            query_params.append(station_id)

        per_page = 10
        offset = (page - 1) * per_page
        query += f" LIMIT {per_page} OFFSET {offset}"

        cur = mysql.connection.cursor()
        cur.execute(query, query_params)
        results = cur.fetchall()
        cur.close()

        return [{'id': row[0], 'date': row[1], 'max_temp': row[2], 'min_temp': row[3], 'precipitation': row[4], 'station_id': row[5]} for row in results]



@ns.route('/stats')
class WeatherStats(Resource):
    """
    Class representing the API endpoint for retrieving weather statistics.

    Attributes:
        - None

    Methods:
        get(self): Retrieves weather statistics based on specified query parameters.
    """

    @ns.doc('weather_statistics')
    @ns.expect(api.parser().add_argument('year', type=int, help='Filter by year')
               .add_argument('station_id', type=str, help='Filter by station ID'))
    @ns.marshal_list_with(statistics_model)
    def get(self):
        """
        Retrieve weather statistics based on specified query parameters.

        Returns:
            List: A list of dictionaries representing weather statistics.
        """

        parser = request.args
        year = parser.get('year', type=int)
        station_id = parser.get('station_id', type=str)

        query = """
        SELECT avg_max_temp, avg_min_temp, total_precipitation
        FROM weather_statistics WHERE 1=1
        """
        query_params = []

        if year:
            query += " AND year = %s"
            query_params.append(year)

        if station_id:
            query += " AND station_id = %s"
            query_params.append(station_id)

        cur = mysql.connection.cursor()
        cur.execute(query, query_params)
        results = cur.fetchall()
        cur.close()

        stats = []
        for result in results:
            stats.append({
                'avg_max_temp': float(result[0]) if result[0] else 0.0,
                'avg_min_temp': float(result[1]) if result[1] else 0.0,
                'total_precipitation': float(result[2]) if result[2] else 0.0
            })

        return stats

if __name__ == '__main__':
    app.run(debug=True)
