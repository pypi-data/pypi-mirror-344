# Sidecar Go Package Documentation

This README provides documentation for the `handlers` package of the Sidecar Go application. The `handlers` package contains HTTP request handlers, including the `GetAttributeStatesHandler`, `PostAttributeStatesHandler`, `GetIOMapsSystemHandler`, and `GetIOMapsHandler`. These handlers are responsible for various tasks, including retrieving, creating, and managing attribute states and I/O maps based on query parameters and request bodies.

## Table of Contents

- [Overview](#overview)
- [GetAttributeStatesHandler](#getattributestateshandler)
  - [Request](#request)
  - [Query Parameters](#query-parameters)
  - [Response](#response)
  - [Error Handling](#error-handling)
  - [Dependencies](#dependencies)
  - [Usage](#usage)
  - [Example Usage](#example-usage)
- [PostAttributeStatesHandler](#postattributestateshandler)
  - [Request](#request-1)
  - [Query Parameters](#query-parameters-1)
  - [Request Body](#request-body)
  - [Response](#response-1)
  - [Error Handling](#error-handling-1)
  - [Dependencies](#dependencies-1)
  - [Usage](#usage-1)
  - [Example Usage](#example-usage-1)
- [GetIOMapsSystemHandler](#getiomapssystemhandler)
  - [Request](#request-2)
  - [Query Parameters](#query-parameters-2)
  - [Response](#response-2)
  - [Error Handling](#error-handling-2)
  - [Dependencies](#dependencies-2)
  - [Usage](#usage-2)
  - [Example Usage](#example-usage-2)
- [GetIOMapsHandler](#getiomapshandler)
  - [Request](#request-3)
  - [Query Parameters](#query-parameters-3)
  - [Response](#response-3)
  - [Error Handling](#error-handling-3)
  - [Dependencies](#dependencies-3)
  - [Usage](#usage-3)
  - [Example Usage](#example-usage-3)
- [Contact Information](#contact-information)

## Overview

The `handlers` package contains HTTP request handlers for the Sidecar Go application. This README provides documentation for the various handlers, including those for attribute states and I/O maps.

## GetAttributeStatesHandler

The `GetAttributeStatesHandler` function is responsible for handling HTTP GET requests to retrieve attribute states based on query parameters. This handler processes incoming requests, extracts query parameters, generates attribute fully qualified names (AttributeFQN), and returns the corresponding attribute states in JSON format.

### Request

- **HTTP Method:** GET
- **Endpoint:** `/attributeStates`

### Query Parameters

The following query parameters can be included in the GET request to filter attribute states:

- `system_name`: The name of the system for which attribute states are requested.
- `component_name`: The name of the component for which attribute states are requested.
- `connector_name`: The name of the connector for which attribute states are requested.
- `instrument_name`: The name of the instrument for which attribute states are requested.
- `attribute_name`: The name of the attribute for which attribute states are requested.

### Response

- **HTTP Status Codes:**
  - `200 OK`: The request was successful, and the attribute states were found.
  - `400 Bad Request`: An error occurred while processing the request (e.g., invalid query parameters).
  - `404 Not Found`: The requested attribute or attribute state was not found.
  - `500 Internal Server Error`: An error occurred while processing the response.

- **Response Body:** The response body contains a JSON object with the following structure:

```json
{
  "value": {
    "timestamp": "2023-09-19T16:17:39.021067+00:00",
    "id": "CATR7C69962F66305817BFD73606BCD112D4",
    "stateSchemaId": "paracloud.ai/schemas/control-task-app-demo/attribute/state/BatchCmd",
    "state": {
      "abort": false,
      "hold": false,
      "load": false,
      "path": "",
      "restart": false,
      "start": false
    }
  }
}
```

- **Example Response (200 OK):**

```json
{
  "value": {
    "timestamp": "2023-09-19T16:17:39.021067+00:00",
    "id": "CATR7C69962F66305817BFD73606BCD112D4",
    "stateSchemaId": "paracloud.ai/schemas/control-task-app-demo/attribute/state/BatchCmd",
    "state": {
      "abort": false,
      "hold": false,
      "load": false,
      "path": "",
      "restart": false,
      "start": false
    }
  }
}
```

- **Example Response (404 Not Found):**

```json
{
  "error": "Attribute not found"
}
```

### Error Handling

- If there are errors during query parameter extraction, attribute retrieval, or response marshaling, the handler responds with an appropriate HTTP error code and message.
- Ensure that the error responses provide clear information about the nature of the error.

### Dependencies

- This handler relies on various components and dependencies, including:

  - `jsonMarshalFunc` (wrapper function for `json.Marshal`)
  - `HandlerParams` (parameters passed to the handler)
  - Caches (e.g., `StateCache`, `AttributeCache`, `ConsumerCache`)
  - Attribute retrieval functions (e.g., `FindAttributeInStructure`, `GetAttributeState`)

### Usage

To retrieve attribute states, send a GET request to the `/attributeStates` endpoint with the appropriate query parameters. The handler will process the request and return the attribute state in JSON format.

### Example Usage

```bash
# Send a GET request to retrieve an attribute state
curl -X GET "http://localhost:5060/attributeStates?system_name=example_system&component_name=example_component&connector_name=example_connector&instrument_name=example_instrument&attribute_name=example_attribute"
```

This example demonstrates how to use the `GetAttributeStatesHandler` to fetch attribute states based on query parameters.

## PostAttributeStatesHandler

The `PostAttributeStatesHandler` function is responsible for handling HTTP POST requests to create attribute states based on query parameters and request body. This handler processes incoming requests, extracts query parameters, generates attribute fully qualified names (AttributeFQN), and creates new attribute states with the provided data.

### Request

- **HTTP Method:** POST
- **Endpoint:** `/attributeStates`

### Query Parameters

The following query parameters can be included in the POST request to specify the attribute and its state:

- `system_name`:

 The name of the system for which the attribute state will be created.
- `component_name`: The name of the component for which the attribute state will be created.
- `connector_name`: The name of the connector for which the attribute state will be created.
- `instrument_name`: The name of the instrument for which the attribute state will be created.
- `attribute_name`: The name of the attribute for which the attribute state will be created.

### Request Body

- The request body should contain a JSON object representing the new attribute state to be created.

### Response

- **HTTP Status Codes:**
  - `200 OK`: The request was successful, and the new attribute state was created.
  - `400 Bad Request`: An error occurred while processing the request (e.g., invalid query parameters or request body).
  - `500 Internal Server Error`: An error occurred while processing the response.

- **Example Request Body:**

```json
{
  "name": "",
  "pv": 8,
  "net": 0.0,
  "tare": 0.0,
  "tare_cmd": false,
  "tare_state": false
}
```

#### Error Handling

- If there are errors during query parameter extraction, request body parsing, attribute creation, or response handling, the handler responds with an appropriate HTTP error code and message.
- Ensure that the error responses provide clear information about the nature of the error.

#### Dependencies

- This handler relies on various components and dependencies, including:

  - `fmt` (for error handling and formatting)
  - `http` (for HTTP response handling)
  - `time` (for timestamp generation)
  - Other components related to attribute handling (e.g., `StateCache`, `AttributeCache`, `StructureFinder`)

#### Usage

To create new attribute states, send a POST request to the `/attributeStates` endpoint with the appropriate query parameters and request body. The handler will process the request, create the attribute state, and respond with an appropriate status code.

### Example Usage

```bash
# Send a POST request to create a new attribute state
curl -X POST http://localhost:5060/attributeStates?system=Pixer%20Solo%20Mule%20-%20Sidecar%20Test%201&component=Buffer%20concentrate&connector=&instrument=wit01&attribute=cmd
Content-Type: application/json

{
  "name": "",
  "pv": 8,
  "net": 0.0,
  "tare": 0.0,
  "tare_cmd": false,
  "tare_state": false
}
```

This example demonstrates how to use the `PostAttributeStatesHandler` to create new attribute states based on query parameters and request body.

## GetIOMapsSystemHandler

The `GetIOMapsSystemHandler` function is responsible for handling HTTP GET requests to retrieve I/O maps for a specific system based on query parameters. This handler processes incoming requests, extracts query parameters (`system_name`), retrieves or caches the system's ID, and fetches I/O maps associated with that system.

### Request

- **HTTP Method:** GET
- **Endpoint:** `/ioMapsSystem`

### Query Parameters

The following query parameters can be included in the GET request to filter I/O maps for a specific system:

- `system_name`: The name of the system for which I/O maps are requested.

### Response

- **HTTP Status Codes:**
  - `200 OK`: The request was successful, and the I/O maps were found.
  - `400 Bad Request`: An error occurred while processing the request (e.g., missing or invalid query parameters).
  - `500 Internal Server Error`: An error occurred while processing the response.

- **Response Body:** The response body contains a JSON array of I/O map data for the specified system.

```json
[
  {
  "component": "Pixer",
  "connector": "",
  "instrument": "pump01",
  "attribute": "state",
  "io_map": {
    "id": "CIOM36A6CB30E5A740D7A2FDBE544EF8BDC5",
    "createdAt": "2023-09-19T15:25:46.267246+00:00",
    "createdBy": "USER95FDBC9B377445ADBF1B9F5CDE118A78",
    "modifiedAt": "2023-09-19T15:25:46.267246+00:00",
    "modifiedBy": "USER95FDBC9B377445ADBF1B9F5CDE118A78",
    "name": "state",
    "parent": "CATRC507E33F8E965A37BD111AD1026D1C08",
    "version": 0,
    "deleted": false,
    "maps": [
      {
        "key": "unique_id",
        "value": "xcvuopdsf9"
      },
      {
        "key": "model",
        "value": "AKD"
      },
      {
        "key": "vendor",
        "value": "KollMorgen"
      },
      {
        "key": "description",
        "value": "Used to populate config page"
      },
      {
        "key": "protocol",
        "value": "Static"
      },
      {
        "key": "address",
        "value": "192.168.1.15"
      }
    ]
  }
},
  ...
]
```

### Error Handling

- If there are errors during query parameter extraction, system ID retrieval, I/O map fetching, or response marshaling, the handler responds with an appropriate HTTP error code and message.
- Ensure that the error responses provide clear information about the nature of the error.

### Dependencies

- This handler relies on various components and dependencies, including:

  - Caches (e.g., `SystemIDCache`, `IOMapsCache`)
  - I/O map retrieval functions (e.g., `GetSystemByNameProxy`, `GetIOMapsBySystemProxy`)

### Usage

To retrieve I/O maps for a specific system, send a GET request to the `/ioMapsSystem` endpoint with the `system_name` query parameter. The handler will process the request and return the I/O maps in JSON format.

### Example Usage

```bash
# Send a GET request to retrieve I/O maps for a specific system
curl -X GET "http://localhost:5060/ioMapsSystem?system_name=example_system"
```

This example demonstrates how to use the `GetIOMapsSystemHandler` to fetch I/O maps for a specific system based on query parameters.

## GetIOMapsHandler

The `GetIOMapsHandler` function is responsible for handling HTTP GET requests to retrieve I/O maps based on query parameters. This handler processes incoming requests, extracts query parameters, generates query keys, and retrieves relevant I/O maps from the cache.

### Request

- **HTTP Method:** GET
- **Endpoint:** `/ioMaps`

### Query Parameters

The following query parameters can be included in the GET request to filter I/O maps:

- `system`: The name of the system to filter I/O maps (e.g., `Pixer Solo Mule - Sidecar Test 1`).
- `component`: The name of the component to filter I/O maps.
- `attribute`: The name of the attribute to filter I/O maps.
- `instrument`: The name of the instrument to filter I/O maps.
- `maps_query`: Additional query parameters to filter I/O maps based on specific attributes (e.g., `model=AKD`, `vendor=Kollmorgen`, `unique_id=123456`).

In this example, the request is made to filter I/O maps for the specified system (`Pixer Solo Mule - Sidecar Test 1`) and further narrow down the results using the `model=AKD` filter in the `maps_query` parameter.

### Response

- **HTTP Status Codes:**
  - `200 OK`: The request was successful, and the matching I/O maps were found.
  - `400 Bad Request`: An error occurred while processing the request (e.g., invalid query parameters).
  - `500 Internal Server Error`: An error occurred while processing the response.

- **Response Body:** The response body contains a JSON array of I/O map data that matches the query parameters.

```json
[
  {
    "SystemName": "Pixer Solo Mule - Sidecar Test 1",
    "ComponentName": "Pixer",
    "ConnectorName": "",
    "InstrumentName": "pump01",
    "AttributeName": "state",
    "IOMapName": "state",
    "Maps": [
      {
        "key": "unique_id",
        "value": "xcvuopdsf9"
      },
      {
        "key": "model",
        "value": "AKD"
      },
      {
        "key": "vendor",
        "value": "KollMorgen"
      },
      {
        "key": "description",
        "value": "Used to populate config page"
      },
      {
        "key": "protocol",
        "value": "Static"
      },
      {
        "key": "address",
        "value": "192.168.1.15"
      }
    ]
  }
]
```

### Error Handling

- If there are errors during query parameter extraction, query key generation, I/O map retrieval, or response marshaling, the handler responds with an appropriate HTTP error code and message.
- Ensure that the error responses provide clear information about the nature of the error.

### Dependencies

- This handler relies on various components and dependencies, including:

  - Caches (e.g., `IOMapsCache`)
  - I/O map retrieval functions (e.g., `FindValuesBySubString`, `FindValuesByMapsData`)

### Usage

To retrieve I/O maps, send a GET request to the `/ioMaps` endpoint with the appropriate query parameters. The handler will process the request and return the matching I/O maps in JSON format.

### Example Usage

```bash
# Send a GET request to retrieve I/O maps based on query parameters
curl -X GET http://localhost:5060/ioMaps?system=Pixer%20Solo%20Mule%20-%20Sidecar%20Test%201&component=&attribute=&instrument=&maps_query=model%3DAKD

```

This example demonstrates how to use the

 `GetIOMapsHandler` to fetch I/O maps based on query parameters.

## Contact Information

For any issues or questions related to these handlers or the Sidecar service, please contact our support team at support@sidecar.io.

## Contributing

Authenticate with AWS Private PyPi before `poetry install`

```sh
export AWS_PROFILE=artifacts
./scripts/auth.sh
poetry env use 3.11
poetry install
```

Ready to go!

## Publish to ConSynSys AWS Private PyPi

```sh
export AWS_PROFILE=artifacts
./scripts/auth.sh
./scripts/publish.sh
```