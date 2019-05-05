# TFLflaskapp
This is an application that returns live bus arrival times using TFL api.

```https://api.tfl.gov.uk/StopPoint/490009333W/arrivals```

## Installing

1. Clone this gitHub repository


2. Activate the virtual environment

   ```source TFLflaskapp/venv/bin/activate```
   

3. Set the following environmental variables to setup your database 

    ```export DB_USER= YOUR_DB_USERNAME ```

    ```export DB_NAME= YOUR_DB_NAME  ``` If not set will default to ```tfl```

    ```export DB_PASS= YOUR_DB_PASSWORD  ```

    ```export DB_HOST= PREFERED_HOST  ``` If not set will default to ```local host```


4. Optional: To set debug environment

   ```export FLASK_ENV=development ```
   
   ``` export FLASK_DEBUG=true ```
   
## Built with

Python flask framework
Psycopg2 adapter with PostgreSQL
