# TFLflaskapp
This is an application that returns live bus arrival times using TFL api.

```https://api.tfl.gov.uk/StopPoint/490009333W/arrivals```

This app contains two pages.
   1. Home page:
   
      Displays the live bus arrivals for bus route K1
      
   2. History page:
   
      Displays the history of the bus arrival times and timestamps when the api call is made
      
      
## Installing

1. Clone this gitHub repository

   ```
   git clone git@github.com:TaniyaAmidon/TFLflaskapp.git
   ```

2. Activate the virtual environment

   ``` cd TFLflaskapp ```
   
  ``` source venv/bin/activate ```
   

3. Set the following environmental variables to setup your database by running the below commands in the terminal

    ```export DB_USER= YOUR_DB_USERNAME ```

    ```export DB_NAME= YOUR_DB_NAME  ```

    ```export DB_PASS= YOUR_DB_PASSWORD  ```

    ```export DB_HOST= PREFERED_HOST  ``` If not set will default to ```local host```


4. Optional: To set debug environment

   ```export FLASK_ENV=development ```
   
   ``` export FLASK_DEBUG=true ```
   
## Built with

Python flask framework
Psycopg2 adapter with PostgreSQL
