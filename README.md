
# Oxford Rivers Portal API (Python Wrapper)

A Python library for accessing and processing data from the  
**Oxford Rivers Portal** (https://oxfordrivers.ceh.ac.uk/).

## Quickstart
To build locally, you'll need to run
```commandline
pipenv install
```
A demo is available in `src/oxrivers_api/demo.ipynb`.

The library comes in three parts. 

### API client to get JSON data
The first is the API to JSON client
which wraps called to the Oxford Rivers API and stores the JSON
result locally. Unless you want JSON data on its own, skip to the loader below
to get the data in pandas format.

```python
from pathlib import Path
from oxrivers_api.storage.json_storage import LocalJsonStorage
from oxrivers_api.api_to_json_client import APIToJson
from oxrivers_api.data_loaders.json_to_pandas_loader import JsonToPandasLoader
from oxrivers_api.models.request_models import TimeseriesInfo

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
from oxrivers_api.storage.json_storage import LocalJsonStorage
from oxrivers_api.api_to_json_client import APIToJson
from oxrivers_api.data_loaders.json_to_pandas_loader import JsonToPandasLoader
from oxrivers_api.models.request_models import TimeseriesInfo

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

### Experimental: The data cache
The data cache is helper that will allow you to store requests as pandas
in a dictionary-like way. The most helpful part is that the keys of the dictionary
are descriptive, even if the ids of the sites and determinands are numbers, because
the default key maps the id to a name first.

```python
import pandas as pd
from matplotlib import pyplot as plt

from oxrivers_api.models.request_models import TimeseriesInfo, DataForDateInfo
from oxrivers_api.data_cache import DataCache
from oxrivers_api.data_loaders.json_to_pandas_loader import JsonToPandasLoader
from pathlib import Path
from pprint import pprint

import matplotlib

from oxrivers_api.api_to_json_client import APIToJson
from oxrivers_api.storage.json_storage import LocalJsonStorage

# choose where to store json locally
data_dir: Path = Path("../data")

# set up Oxford Rivers Client and Pandas loader
storage = LocalJsonStorage(data_dir)
client = APIToJson(storage)
loader = JsonToPandasLoader(client)

# Example usage to get and store time series data for fft in Oxford:
cache = DataCache(loader)
siteID = "Oxford"
cache.get_timeseries(TimeseriesInfo("fft", siteID))
cache.get_data_for_date(DataForDateInfo("rainfall", "2022-05-05"))

# list contents in cache
pprint(cache.contents())

# display fft data
fft_oxford = cache.get_by_key("fft_Oxford_None")

# plot fft data daily average
fft_oxford['datetime'] = pd.to_datetime(fft_oxford['datetime'])
fft_oxford.set_index('datetime', inplace=True)
fft_oxford = fft_oxford.dropna(subset="value")
fft_oxford = fft_oxford.resample('D').mean(numeric_only=True)
fft_oxford["value"].plot()
# use datasets data to label plot - it's already populated in the cache
dataset_description = cache.datasets[cache.datasets["id"]=="fft"].iloc[0]["name"] + " for " + siteID
plt.title(dataset_description)
yaxis_label = "treatment (l/s)" # This is unavailable from the dataset info
plt.ylabel(yaxis_label)
plt.show()
```