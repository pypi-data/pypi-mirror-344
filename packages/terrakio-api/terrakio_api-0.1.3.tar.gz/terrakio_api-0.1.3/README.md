# Terrakio API Client

A Python client for Terrakio's Web Coverage Service (WCS) API.

## Installation

Install the package using pip:

```bash
$ pip install terrakio-api==0.1.3
```

## Configuration

1. Obtain a Personal Access Token:
   - Open the following link for the terrakio_doc - https://test-341.gitbook.io/terrakio/terrak.io/authentication
   - Sign up for the terrakio platform illustrated in the doc
   - Log in for the terrakio platform illustrated in the doc
   - Generate the key for the platform
   - The above generate command should have generated a config file (`~/.tkio_config.json`), in which it stores the EMAIL and the TERRAKIO_API_KEY
   - The personal access key is being stored here

## Important Notes
- Always review and agree to the Terms and Conditions for each dataset you intend to download.

# Test

Perform a small test retrieve of precipitation_m15 data:

```
import terrakio_api
from terrakio_api import Client
from terrakio_api.utils import create_point_feature
# 1. Initialize the client
client = Client()  # This will read from ~/.tkio_config.json, which will get the your api key, the default url for the server is https://terrakio-server-candidate-d4w6vamyxq-ts.a.run.app/wcs_secure
# 2. Create a geographic feature (point)
point = create_point_feature(lon=149.057, lat=-35.1548)
# 3. Make a WCS request
dataset = client.wcs(
     expr="prec=RainfieldsCBR.precipitation_m15@(year=2024, month=1)\nprec",
     feature=point,
     output="netcdf"  # Specify output format (csv, netcdf, etc.)
     )
# 4. Work with the resulting xarray dataset
print(dataset)

# If you want to change the key, you could either pass the new key to the Client function like client = Client( key = NEW_KEY ) or just go into the ~/.tkio_config.json file and change it manually.
# If you want to change the url, you could just pass the new url to the Client function like client = Client( url = NEW_URL )
```


# License

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

In applying this licence, ECMWF does not waive the privileges and immunities granted to it by virtue of its status as an intergovernmental organisation nor does it submit to any jurisdiction.