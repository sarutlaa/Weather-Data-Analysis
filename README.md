
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
## APIs Unit Testing

For unit testing, apis_unit_testing.py imports app.py to conduct tests on the query parameters specified for both API endpoints. This process utilizes pytest, TestCase, and the flask_testing Python libraries.
## Approach for AWS Deployment
