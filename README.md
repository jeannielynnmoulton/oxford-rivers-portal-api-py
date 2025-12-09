
# Oxford Rivers Portal API (Python Wrapper)

A Python library for accessing and processing data from the  
**Oxford Rivers Portal** (https://oxfordrivers.ceh.ac.uk/).

## Quickstart
To build locally, you'll need to run
```commandline
pipenv install
```
A demo is available in `src/oxrivers_api/demo.ipynb`.

The library comes in two parts. 

### API client to get JSON data
The first is the API to JSON client
which wraps called to the Oxford Rivers API and stores the JSON
result locally. Unless you want JSON data on its own, skip to the loader below
to get the data in pandas format.

```python
from pathlib import Path
from src.oxrivers_api.storage.json_storage import LocalJsonStorage
from src.oxrivers_api.api_to_json_client import APIToJson
from src.oxrivers_api.data_loaders.json_to_pandas_loader import JsonToPandasLoader
from src.oxrivers_api.models.request_models import TimeseriesInfo

data_dir = Path("../data")
storage = LocalJsonStorage(data_dir)
client = APIToJson(storage)
# The client enables you to get the json data directly by
# return the path the json file
json_file = client.get_timeseries("fft", "Oxford")
print(json_file)
```

### JSON to pandas loader
The second part is a loader that wraps the above client and will make API calls,
store json locally and load it as a pandas dataframe.

```python
from pathlib import Path
from src.oxrivers_api.storage.json_storage import LocalJsonStorage
from src.oxrivers_api.api_to_json_client import APIToJson
from src.oxrivers_api.data_loaders.json_to_pandas_loader import JsonToPandasLoader
from src.oxrivers_api.models.request_models import TimeseriesInfo

# Using the json to pandas loader will use the client to get the 
# json as well as convert it to a data frame.
data_dir = Path("../data")
storage = LocalJsonStorage(data_dir)
client = APIToJson(storage)
loader = JsonToPandasLoader(client)
time_series_info = TimeseriesInfo("fft", "Oxford")
df = loader.load_timeseries(time_series_info)
print(df.head(10))
# or you can do this directly from the TimeseriesInfo object
df2 = time_series_info.request().as_pandas(loader)
print(df2.head(10))
```
API calls are only made when there is no local json file, so it is efficient to use the client/loader to make repeated calls.

The endpoints and their corresponding info objects are defined in `models/request_models.py`
getDatasets -> DatasetsInfo
getDeterminands -> DeterminandsInfo
getSites -> SitesInfo
getTimeseries -> TimeseriesInfo
getDataForDate -> DataForDateInfo

These can be used to call `.request().as_pandas()` as in the demo code above,
which will make a request to the API and store is as pandas in one line.