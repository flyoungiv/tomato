# Tomato [Backend] 🍅
=======
This code creates a simple FastAPI Python server and provides a few basic endpoints.
Link to frontend repo: https://github.com/flyoungiv/tomato

## To-Do

- ~~FastAPI hello world~~
- ~~generate sample data~~
- ~~set up git repo https://github.com/flyoungiv/tomato~~
- ~~host BE https://fastapi.tiangolo.com/deployment/deta/~~
- ~~fix CORS issues for local~~
- ~~host a db~~
- ~~inject data to db~~
- ~~read data from db~~
- pagination
- search
- filter
- sort
- graph 1: correlation between population and number of medals
- ~~create google cloud db~~
- normalize db table so each contestant has its own uuid
- introduce an ORM (sqlAlchemy?)
- set up auth FE
- set up auth token validation BE
- choose conclusion for data
- link graph to data in table
- add links/metadata section
- set up CI/CD
- scatter plot of total medals per country across all years
- country flag emojis (need alpha 2 country code)

## Data Sources
https://data.worldbank.org/indicator/SP.POP.TOTL
https://www.worlddata.info/countrycodes.php

## Notes & Thoughts
=======
- i could have saved time by only taking matches on ISO and NOC country codes but i wanted to find a solution because real life data is messy
- i don't have homebrew. i don't have anything. what a time to format my computer
- had to find a lookup table for country codes to convert from olympics to iso
- did not get to mobile
- would be better to have done data transformation within endpoint instead of in a separate script
- did not get to auth
- likelihood of reappearance if you win a medal
