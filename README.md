
# Suitepy

<br />

__Python Library for the Netsuite REST API__

<br />

_will update this README later into a cleaner version with better examples, just getting a starting point established for now_

<br />

## Installation
__Currently not in PIP repositories. Will make into a Package Later__ <br />
~~pip install suitepy~~

<br />

## Usage

### Setup
netsuite integration and access tokens . . .<br />
production and sandbox account id in url . . . <br />
<br />
Credentials should be a JSON Object with the following parameters __NOTE: These are fake example Tokens__

```json
{
    "account_id": "4747815",

    "token_id": "12345abcde678910fghij123asdf234asdfwr5sdaf2354sadg234sadf234dsaf",
	
    "token_secret": "saf8u9as79823623h4nfy7324uihfe78428h78nhew789823fm782387n8372h72",
	
	"consumer_key": "askjdhfuiy3278950234875hfjhsdkf3287942346shf349875hsdf8734hdfsi7",
	
	"consumer_secret": "sdaf6987sf6873hi5h34k57fd78sd623h4n3k8d9fg7sdf98g7kj5n3k4j5nd897"
}
```

<br />

__Import Suitepy__

```python
import suitepy as sp
```

<br />

Create an instance of __RESTMaster__

```python
meister = sp.RESTMaster(credentials)
```

<br />

### Query
only select . . . <br />
see suiteql documentation and sql-92 stuff . . . <br />
__Query All__
```python
records = meister.query_all("SELECT companyName FROM Customer")

# Convert to a pandas dataframe
import pandas as pd
df = pd.DataFrame(records)
```

<br />

__CRUD opreations return empty HTTP 204 No Content responses on success__<br />
- So you can check response.ok to determine if successful
- Also, it only lets you do things 1 record at a time, but I will make a bulk_create and bulk_update method later

<br />

### Create
empty response on success, check ok and status code . . . <br />
Use the header link that is returned to determine the id of the newly created record, if needed. <br />
create bulk . . . <br />
. . .<br />
__Create__
```python
response = meister.create('customer', '{"entityid": "RESTTEST_1", "companyname": "REST Customer 1", "subsidiary": {"id": "7"}}')

# Check Results
print(response.ok)
print(response.status_code)
```

<br />

### Update
. . . <br />
__Update__
```python
# Need the Internal Id of the record, in this case 124529, later I will work on external id
response = meister.update('customer', 124529, '{"externalId": "REST_Customer_3"}')
```

<br />

### Delete
. . .<br />
__Delete__
```python
# Need the Internal Id of the record, in this case 124530, later I will work on external id
response = meister.delete('customer', 124530)
```

<br />

### Errors
Exceptions . . . <br />
error messages . . . <br />
. . .

<br />

etc.

<br / >

. . .