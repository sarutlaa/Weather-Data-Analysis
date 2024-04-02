
# Weather Data Analysis

This is a coding assessment challenge that involves analyzing weather data from various stations in four phases. The tasks and implementation for each phase are listed below.




## Task 1 : Data Modeling

### Tech Stack

**RDBMS:** MySQL Database

**Language:** Pure SQL

For the Data Modeling Task, I have chosen MySQL Database (RDBMS), where a database name 'corteva' is created with the weather_data as the table.The wx_data encompasses daily weather records for a specific timeframe, including maximum temperature, minimum temperature, and precipitation for each day.  The DDL for the table creation is as follows:

```ruby
CREATE DATABASE corteva;
```

```ruby
CREATE TABLE weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    max_temp DECIMAL(5,2), 
    min_temp DECIMAL(5,2), 
    precipitation DECIMAL(6,2), 
    station_id TEXT NOT NULL,
    UNIQUE KEY unique_date_station (date, station_id) 
);
```

*Data Model Design:*
* id: Unique identifier for each weather record (auto-increments)
* date: Date of the weather record (NOT NULL)
* max_temp: Maximum temperature for the day (in degrees Celsius)
* min_temp: Minimum temperature for the day (in degrees Celsius)
* precipitation: Total precipitation for the day (in centimeters)
* station_id: Unique identifier for the weather station (NOT NULL)
* unique_date_station : Ensures that there are no duplicate entries for a combination of date and station_id.This constraint ensures that there are no duplicate entries for a combination of date and station_id, preventing redundancy and ensuring data integrity, especially when the code is executed multiple times.





## Task 2 : Data Ingestion


The data files from the wx_data repository on GitHub were replicated locally for further processing. The data ingestion process was orchestrated by the Data_Ingestion.ipynb Python notebook. During the ingestion, missing records represented by -9999 were replaced with NULL values. Additionally, the temperature values were originally in tenths of a degree Celsius, but they were converted to degrees Celsius to match the database format. Similarly, precipitation values, originally in tenths of millimeters, were converted to centimeters.
A total of 1,729,957 records were processed, with the start_time, end_time, duration of data ingestion as shown below.






### Screenshots

![data_ingestion1](https://github.com/sarutlaa/Weather-Data-Analysis/assets/141533429/c1fe0c31-c768-4abc-aec5-d81e1c7edee0)



## Task 3: Data Analysis
The necessary aggregations have been computed and stored in a separate table named weather_statistics whose schema is defined as below.

```ruby
CREATE TABLE weather_statistics (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    station_id VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    avg_max_temp DECIMAL(5, 2),
    avg_min_temp DECIMAL(5, 2),
    total_precipitation DECIMAL(6, 2),
    UNIQUE KEY unique_station_year (station_id, year)
);
```
*Data Model Design:*
* stat_id: Unique identifier for each weather statistic record (auto-increments)
* station_id: Unique identifier for the weather station (NOT NULL)
* year: Year for which the statistics are calculated (NOT NULL)
* avg_max_temp: Average maximum temperature for the year (in degrees Celsius)
* avg_min_temp: Average minimum temperature for the year (in degrees Celsius)
* total_precipitation: Total accumulated precipitation for the year (in centimeters)
* unique_station_year: Ensures that there are no duplicate entries for a combination of station_id and year. This constraint ensures that there are no duplicate entries for a combination of station_id and year, preventing redundancy and ensuring data integrity in the context of the weather data.

The aggrgations have been performed and then ingested into weather_statistics table in the Data_Analysis.ipynb file. In total 4791 records have been processed and stored. Records with missing values have been ignored.

### Screenshots

![data_ingestion2](https://github.com/sarutlaa/Weather-Data-Analysis/assets/141533429/ae9a80ec-4f7e-4915-9fe3-94c6ebb008e9)



```ruby
SELECT station_id, count(*) FROM corteva.weather_statistics
group by station_id;
```
The year wise count output is stored in weather_stats_output.csv


## Task 4: Rest API
### Tech Stack

**Frameworks:** 
- Flask
- Flask-RESTx ( For Easy RESTful API Development)
- Flask-MySQLdb ( For  Direct Database Access)
- Swagger(OpenAI) ( For Standardized Documentation)


For this project, the Flask framework has been chosen to manage interactions with two key tables: weather_data and weather_statistics, which are accessible via specific API endpoints. The app.py Python script is responsible for setting up these API endpoints.

By executing app.py present in the weather_api directory, the application initiates connections to these endpoints. This configuration enables users to perform queries and apply filters based on defined criteria.

## API Reference

#### Get all items

```http
  GET /api/weather
```

The specified endpoint fetches a collection of records from the weather_data table within the corteva database. Users can manage the output using pagination and apply filters based on the parameters outlined below.


Add the table here

```http
  GET /api/weather/stats
```
| Query Parameters | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `page` | `integer` | Optional. The page number of the results. Default is 1|
| `per_page` | `integer` | Optional. The page number of the results. Default is 10|
| `date` | `string` |Optional. Filters results to this specific date (format: YYYY-MM-DD)|
| `station_id` | `string` | Optional. Filters results to the specified station ID|

The specified endpoint accesses a collection of entries from the weather_statistics table in the corteva database. It allows for response manipulation through pagination and utilizes the following parameters for filtering.

| Query Parameters | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `page` | `integer` | Optional. The page number of the results. Default is 1|
| `per_page` | `integer` | Optional. The page number of the results. Default is 10|
| `year` | `string` |Optional. Optional. Filters results to this specific year|
| `station_id` | `string` | Optional. Filters results to the specified station ID|


## APIs Implementation Results

I utilized Postman for testing the functionality of my API endpoints, ensuring data retrieval operations performed as expected. Additionally, Swagger was employed to document the API, providing a clear and interactive interface for exploring its capabilities.

### Postman Screenshots
Utilizing Postman to assess the functionality of Weather API.
1. GET method to access [http://127.0.0.1:5000/weather/api](http://localhost:5000/api/weather)
   
    ![postman_weather_api](https://github.com/sarutlaa/Weather-Data-Analysis/assets/141533429/10dc0038-e225-4cd1-9e4d-3fe4f5676069)
3. GET method to access [http://127.0.0.1:5000/weather/api](http://localhost:5000/api/weather/?date=1985-01-01&station_id=USC00332098)

    ![postman_weather_api_param](https://github.com/sarutlaa/Weather-Data-Analysis/assets/141533429/31c1ba1c-a69a-4b28-9522-f8f6dd5729bd)
4. GET method to access [http://127.0.0.1:5000/weather/api/stats](http://localhost:5000/api/weather/stats)

    ![postman_warther_api_stats](https://github.com/sarutlaa/Weather-Data-Analysis/assets/141533429/2cd268c2-1584-4faa-8d8d-84be3176f3e4)
4. GET method to access http://localhost:5000/api/weather/stats?year=1985&station_id=USC00253660
   
    ![postman_weather_api_stats_param](https://github.com/sarutlaa/Weather-Data-Analysis/assets/141533429/96829b12-06a3-43d7-b16d-530428ef2c73)

### Swagger(OpenAI) Screenshots

Utilizing Swagger UI to assess the functionality of Weather API. This interface serves as an interactive API documentation that allows for:

- Running a local server, indicated by the http://127.0.0.1:5000 URL.
- Providing two GET endpoints for accessing weather data and weather statistics.
- Outlining the data models for the API responses, including weather information and statistical data.

    ![swagger_overview](https://github.com/sarutlaa/Weather-Data-Analysis/assets/141533429/e7cf1731-f23a-4c6c-bc49-98de8fec37ce)

1. GET method to access to http://127.0.0.1:5000/api/weather/?page=1&date=1996-01-02&station_id=USC00184108
   Date : 1986-01-02, station_id : USC00114108

    ![swagger_1](https://github.com/sarutlaa/Weather-Data-Analysis/assets/141533429/62fca457-2679-404f-b372-d841f8795e93)

2. GET method access to http://127.0.0.1:5000/api/weather/stats?year=2018&station_id=USC00137147
    year = 2012, station_id : USC00137147

    ![swagger_2](https://github.com/sarutlaa/Weather-Data-Analysis/assets/141533429/869516e7-ee6e-4f1f-a62c-c3416ba9e931)




## APIs Unit Testing

In the unit testing script apis_unit_testing.py, the Flask application from app.py is tested to ensure its API endpoints are correctly processing various query parameters. Leveraging the pytest framework and the TestCase class from flask_testing, a suite of tests is applied to the weather API. These tests are strategically designed to confirm that the API responds with a 200 status code—a marker of success—across a range of requests:

- /api/weather/ with no parameters.
- /api/weather/ including a specific date.
- /api/weather/ with a given station ID.
- /api/weather/stats without parameters.
- /api/weather/stats with a specified year.
- /api/weather/stats with a specified station ID.
- 
Running these tests ensures that the API handles query parameters correctly and the endpoints are functioning as expected. The pytest.main() call at the end of the script triggers the execution of the tests when the script is run. All the testcases passed succesfully with the result as shown below.


  ![unittest](https://github.com/sarutlaa/Weather-Data-Analysis/assets/141533429/52ca9284-b627-44e6-8b51-75bacfcdd834)

## Approach for AWS Deployment
Deploying an end-to-end weather data analysis and API service on AWS involves several stages, including database setup, data processing, and finally exposing the processed data via API.

Task 1: Data Modeling.
For relational data storage on AWS, Amazon RDS with a MySQL instance is an excellent option. It supports the use of familiar SQL-based data modeling. You would use the same data model structure as previously mentioned, which is ideal for relational databases such as MySQL offered by Amazon RDS.

Task 2: Data Ingestion
Data collected initially can be efficiently stored in Amazon S3 buckets. To process this data, an AWS Lambda function is used. This serverless compute service enables code execution in response to events such as changes in data within an S3 bucket, making it ideal for data ingestion tasks. The Lambda function can read raw data files from S3, perform any necessary transformations, and then load the data into Amazon RDS MySQL database.

Task 3: Data Analysis
AWS Lambda can be used in conjunction with Amazon RDS to compute and store statistics. A Lambda function can be created to execute SQL queries that calculate the average temperature and total precipitation for each weather station on an annual basis. These results are then saved in a separate table within the RDS database, using a data model designed specifically for storing analytical results.

Task 4: REST API
A REST API is created with a web framework like Flask to make the ingested and computed weather data accessible. AWS provides Elastic Beanstalk as a PaaS solution that simplifies the deployment and scalability of web applications and services, including REST APIs. By deploying the Flask application on Elastic Beanstalk, the API endpoints /api/weather and /api/weather/stats become available. These endpoints return JSON-formatted data and allow filtering based on date and station ID, with data served directly from the Amazon RDS database.

This strategy includes using AWS services to create a scalable, efficient, and fully managed weather data service. From initial data modeling in RDS to final API deployment via Elastic Beanstalk, each component is designed to integrate seamlessly into the AWS ecosystem, resulting in a robust solution for weather data analysis and accessibility.
