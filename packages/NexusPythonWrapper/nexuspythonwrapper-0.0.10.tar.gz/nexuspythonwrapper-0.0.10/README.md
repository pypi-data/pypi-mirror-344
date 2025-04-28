# NEXUS Python Wrapper

---

NexusPythonWrapper is a Python library for interacting with the asset integrity database solution 
from Wood PLC, NEXUS Integrity Centre (IC).

The library is built around the `NexusWrapper` class, which makes connecting to and performing REST 
API calls more convenient. `NexusWrapper` includes BASIC and APIKEY authentication, standard `GET`, `PUT`, 
`POST` and `DELETE` http requests. The `NexusWrapper` has a custom response model called `Result`. `Result`
simply formats the response from the API in a constant way:

```
'status_code': int          # response.status_code
'message':     str          # response.message
'result':      List[Dict]   # contains all the data in the 'rows' key in the raw NEXUS response
'metadata':    Dict         # Includes information e.g., pageSize, startRow, totalRows
```

Helper classes:
- `NexusEndpoints` for easy url creation
- `NexusFilter` for creating a `X-NEXUS-Filter` header used with `GET` requests
- `NexusSort` for creating a `X-NEXUS-SORT` header used with `GET` requests

NEXUS IC REST API Documentation: https://docs.nexusic.com/6.9/ic-web.rest.v2.html

## Features

---

- Simplified session management
- Consistent response handling
- Powerful filtering and sorting helper classes

## Usage

---

### Installation

```
pip install NexusPythonWrapper
```

### Authentication

The `NexusWrapper` class has two authentication methods available, either BASIC or APIKEY. Regardless of 
authentication method the `uri` (IC-Web address) must be provided. This is the domain name or IP address 
of the server where the REST service is endpoint is hosted, e.g., database.nexusic.com

The `NexusWrapper` class has the following parameters:

```
uri:                 str            # 'https://database.nexusic.com/' 
authentication_type: str            # 'BASIC' or 'APIKEY'
api_key:             str = None     # APIKEYs can be obtained per user for NEXUSIC at "Database/Security/User/Login"
username:            str = None     # 'username@nexusic.com'
password:            str = None
logger:              logging.logger = None
ssl_verify:          bool = True
```

The `uri` and `authentication_type` parameters are required. Additionally, the login credential relating
to the selected `authentication_type` must be passed into the `NexusWrapper` class when it is instantiated.

That is when using:`authentication_type == 'APIKEY'`, a `api_key` parameter must be passed to the class.

Similarly, when using: `authentication_type == 'BASIC'`, `username` and `password` parameters must be passed 
to the class.

As such, to instantiate a `NexusWrapper` class and connect to NEXUS IC will look something like this:

```
conn = NexusWrapper(
    uri = 'https://database.nexusic.com/',
    authentication_type = 'BASIC',
    username = 'joe.bloggs@nexusic.com',
    password = 'goodPassword!'
)
```

In the above example, the classes `__init__` method will validate the passed `authentication_type` 
and account credentials (`username` and `password`). If everything is ok, the credentials are Base64 encoded
and a `POST` request is made to the NEXUS REST Service's login endpoint. If successful, a `hash` key is 
returned which will be used for all future requests. The final step of the `__init__` method is to make a
`GET` request to the database's version endpoint, which returns the version and schema of the database.

Now you're connected to the NEXUS Database's REST API. There is a convenient method which prints out the 
connection details:
```
conn.connection_details()
```

Which will print:

```
Database:         https://database.nexusic.com
Database Version: 6.9.XXX
Database Schema:  8.125
User:             Joe Bloggs
License:          write
```

Finally, once authenticated, the generated `hash` key is valid for 60 minutes from the time of the last 
REST API request. To invalidate the `hash` when you're done working with the API, call the logout method:

```
conn.logout()
```

### GET Requests

---

The NEXUS REST API supports three types of `GET` requests:
- `Get Rows`
- `Get Row`
- `Get Row Field`

The `NexusWrapper.get` processes the parameters included with the method class and then determines the
appropriate helper method (`_get_rows`, `_get_row` or `_get_row_field`) based on the request.

The `NexusWrapper.get` method has the following parameters:

```
table_name:             # required: str:  _get_rows / _get_row / _get_row_field: unique database name for a table
key_value: str          # optional: int:  _get_row / _get_row_field: specifies a row in a table
field_name:             # optional: str:  _get_row_field: specifies a field in a table
headers:                # optional: dict: _get_rows: specifies the 'X-NEXUS-Filter' or 'X-NEXUS-Sort'
paginated:              # optional: bool: _get_rows: True by default, gets all rows in the table via pagination
page_size:              # optional: int:  _get_rows: 100 by default, determines the number of rows per request
start_row:              # optional: int:  _get_rows: 0 by default, determines the first row that is return
calculated_values:      # optional: int:  _get_rows / _get_row: True by default, determines if calculated fields in the table are returned
```

A call to get all the rows in a table will look like this:

```
result = conn.get(table_name='Integrity_Assessment', headers=headers, paginated=True)
```

A call to get a subset of rows in a table will look like this:

```
result = conn.get(table_name='Integrity_Assessment', headers=headers, paginated=False, page_size=50, start_row=50)
```

A call to get a single row in a table will look like this:

```
result = conn.get(table_name='Integrity_Assessment', key_value=123)
```

A call to get a field in a row will look like this:

```
result = conn.get(table_name='Integrity_Assessment', key_value=123, field_name='Assessment')
```

It should be noted that, the validation done on the passed objects is only to determine which subsequent call
will be made. Therefore, it is possible to pass additional parameters into the method which won't be used. In
the following example the `headers` passed into the method won't be used, as they are not used to make the 
request in the `_get_row` method, which is determined by the fact that a `table_name` and `key_value` have 
been passed into the method:

```
result = conn.get(table_name='Integrity_Assessment', key_value=123, headers=headers)
```

### PUT Request

---

To create a new row in a table, the NEXUS REST API uses a `PUT` request. Here is an example, adding a new
integrity assessment.

Firstly, set up the request body. This will include all the fields you want to populate in the target table:

```
body = {
    'Component_ID': 1,
    'Assessment_Date': 2025-04-26,
    'Inspection_Date': 2025-04-01,
    'Inspection_Activity': 4,
    'Assessment': 'Light surface corrosion noted throughout the corrosion circuit, not considered an conecrn at this time'
}
```

Make the request:

``` 
result = conn.put(table_name='Integrity_Assessment', request_body=body)
```

The `NexusWrapper.put` method has an optional parameter `calculatedFields`, which determines
if the APIs response includes calculated fields from the table, by default this parameter is `True`.

### POST Request

---

To update a row in a table, the NEXUS REST API uses a `POST` request. Here is an example, updating the assessment
of a row in the integrity assessment table.

Firstly, set up the request body to update selected fields in the target table:

```
body = {
    'Inspection_Date': 2025-04-14,
    'Assessment': 'Severe internal corrosion noted, generally, at the 6 o'clock position of the pipeline.'
}
```

Each row in a NEXUS table has a unique primary key, for a `POST` request this will be the target row:

``` 
result = conn.put(table_name='Integrity_Assessment', key_value=123, request_body=body)
```

The `NexusWrapper.post` method has an optional parameter `calculatedFields`, which determines
if the APIs response includes calculated fields from the table, by default this parameter is `True`.

### DELETE Request

---

To delete a row in a table:

```
result = conn.delete(table_name='Integrity_Assessment', key_value=123)
```

The NEXUS REST API returns no content in the return response object when a row is deleted. Therefore,
it was decided that in this wrapper library a `GET` request would be made before the row is deleted and
appended to the returned `Result` object so the user has full visibility of what was contained in the
deleted row.