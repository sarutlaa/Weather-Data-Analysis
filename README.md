
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
* unique_date_station : Ensures that there are no duplicate entries for a combination of date and station_id





## Task 2 : Data Ingestion


The data files from wx_data were replicated locally after being sourced from the specified GitHub repository. The task of data ingestion in batches is performed by the Data_Ingestion.ipynb Python notebook. A total of 1,729,957 records were processed.






### Screenshots

![data_ingestion](https://github.com/sarutlaa/Weather-Data-Analysis/assets/141533429/c1fe0c31-c768-4abc-aec5-d81e1c7edee0)



## Task 3: Data Analysis
The required aggrgations have been performed and stored in another table called weather_statistics whose schema is as below. 

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
* unique_station_year: Ensures that there are no duplicate entries for a combination of station_id and year 

The aggrgations have been performed and then ingested into weather_statistics table in the Data_Analysis.ipynb file. In total 4791 records have been processed and stored. Records with missing values have been ignored.The below output is stored in additional files folder of this repo.
```ruby
SELECT station_id, count(*) FROM corteva.weather_statistics
group by station_id;
```


## Task 4: Rest API
### Tech Stack

**Frameworks:** 
- Flask
- Flask-RESTx ( For Easy RESTful API Development)
- Flask-MySQLdb ( For  Direct Database Access)
- Swagger(OpenAI) ( For Standardized Documentation)


For this project, I've selected the Flask framework to facilitate interactions with two primary tables: weather_data and weather_statistics. These tables are accessed through designated API endpoints.

Within the weather_api directory, running app.py establishes connections to these endpoints. This setup allows users to query and filter data according to specified criteria.

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

The specified endpoint accesses a collection of entries from the weather_statistics table in the corteva database. It allows for response manipulation through pagination and utilizes the following parameters for filtering.


## APIs Implementation Results

I utilized Postman for testing the functionality of my API endpoints, ensuring data retrieval operations performed as expected. Additionally, Swagger was employed to document the API, providing a clear and interactive interface for exploring its capabilities.
## APIs Unit Testing

For unit testing, apis_unit_testing.py imports app.py to conduct tests on the query parameters specified for both API endpoints. This process utilizes pytest, TestCase, and the flask_testing Python libraries.
## Approach for AWS Deployment
