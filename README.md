# Async httpx scraper + FastAPI + rabbitMQ


### Start app with docker-compose
    docker-compose up --build

###### check 
web `localhost:8000`

postgres `localhost:5050`

rabbitMQ `localhost:15672` 

### Create tables in database by runing migrations

    docker exec web alembic revision --autogenerate -m 'migration_1'
    docker exec web alembic upgrade head

### Scraping

    docker exec -it web bash

###### Next commands run from docker console

1.Scrape item urls 

    python async_scrap_on_fastapi/scrap/urls_scrap.py

###### here you can chose 1 from 10 regions, or select `all` (u will see it in console)

```
{
    1: ('b-apartments-condos/city-of-toronto', 'c37l1700273'),
    2: ('b-immobilier/ville-de-quebec', 'c34l1700124'),
    3: ('b-apartments-condos/nova-scotia', 'c37l9002'), 
    4: ('b-apartments-condos/new-brunswick', 'c37l9005'), 
    5: ('b-apartments-condos/manitoba', 'c37l9006'),
    6: ('b-apartments-condos/british-columbia', 'c37l9007'),
    7: ('b-apartments-condos/prince-edward-island', 'c37l9011'),
    8: ('b-apartments-condos/saskatchewan', 'c34l9009'),
    9: ('b-apartments-condos/alberta', 'c37l9003'),
    10: ('b-apartments-condos/newfoundland', 'c37l9008'),
    'all': 'Get all regions'
}
```

2. Scrape items data 

    python async_scrap_on_fastapi/scrap/item_scrap.py


3. Insert data to database

    python async_scrap_on_fastapi/repositories/consumer_database.py

### Important

Some requests have not valid response, so url with bad response collecting to separate queue in rabbitMQ

4. Retry scrape urls from step 1

    python async_scrap_on_fastapi/scrap/retry_url_scrap.py

5. Retry scrape items from step 2

    python async_scrap_on_fastapi/scrap/retry_item_scrap.py


### Finaly you can make requests to fetch data from database

'POST', `http://localhost:8000/items?page=1&limit=10`

###### required body

```
{
  "filters": {
  },
  "order_by": {  
  }
}
```

###### possible filters

```
{
  "filters": {
    "ad_id": "string",
    "creator_id": 0,
    "title": "string",
    "location": "string",
    "address": "string",
    "published_date": [
      "2022-11-20", "2022-11-20"
    ],
    "price": [
      0, 2000
    ],
    "hydro": true,
    "heat": true,
    "water": true,
    "wifi": true,
    "parking": 0,
    "agreement_type": "string",
    "move_in_date": "string",
    "pet_friendly": "string",
    "size": [
      0, 2000
    ],
    "furnished": true,
    "laundry_in_unit": true,
    "lundry_in_building": true,
    "dishwasher": true,
    "fridge": true,
    "air_conditioning": true,
    "balcony": true,
    "yard": true,
    "smoking_permitted": true
  },
  "order_by": {
    "order_by": [
      "published_date", "price"
    ]
  }
}
```
