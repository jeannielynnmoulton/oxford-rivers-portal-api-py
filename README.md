# Oxford Rivers Portal API (Python Wrapper)

A Python library for accessing and processing data from the  
**Oxford Rivers Portal** (https://oxfordrivers.ceh.ac.uk/).

## Quickstart
Install the dependences:
```commandline
pipenv install
```
Create a storage mechanism and set up the API client, then you can explore the data.
```python
data_dir = "../data"
storage = JsonSt
```

The main entry point is `api_to_json.py`, which gives methods for exploring data:
- `getDatasets`
- `getDeterminands`
- `getSites(datasetID)`
- `getTimeseries(datasetID, siteID, determinand)`
- `getDataForDate(datasetID, date)`

This class automatically takes care of 