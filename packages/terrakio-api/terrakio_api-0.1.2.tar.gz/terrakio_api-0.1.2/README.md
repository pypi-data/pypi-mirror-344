# Terrakio API Client

A Python client for Terrakio's Web Coverage Service (WCS) API.

## Installation

Install the package using pip:

```bash
$ pip install terrakio-api==0.1.2
```

## Configuration

1. Obtain a Personal Access Token:
   - Install the CLI
   
   - Generate your Personal Access Token

2. Create a configuration file (`~/.tkioapirc`) with the following content:
   ```
   url: https://terrakio-server-candidate-d4w6vamyxq-ts.a.run.app/wcs_secure
   key: <PERSONAL-ACCESS-TOKEN>
   ```

## Important Notes
- Always review and agree to the Terms and Conditions for each dataset you intend to download.

# Test

Perform a small test retrieve of precipitation_m15 data:

```
import terrakio_api
from terrakio_api import Client
from terrakio_api.utils import create_point_feature
# 1. Initialize the client
client = Client()  # This will read from ~/.tkioapirc
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
```


# License

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

In applying this licence, ECMWF does not waive the privileges and immunities granted to it by virtue of its status as an intergovernmental organisation nor does it submit to any jurisdiction.