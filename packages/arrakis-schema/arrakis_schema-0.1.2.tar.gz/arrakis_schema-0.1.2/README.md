# Arrakis Schema Specification

This repository defines the schema for all data, metadata and API requests for
the `arrakis` LIGO data distribution system.

Schemas are defined in one of two places:

* `endpoints/`: Endpoints served from Arrakis server
* `publication/`: Data published into Kafka

## Endpoints

The Arrakis server responds to API requests corresponding to the four
main actions exposed by the client API:

* **stream**: [endpoints/stream](endpoints/stream)
* **describe**: [endpoints/describe](endpoints/describe)
* **find**: [endpoints/find](endpoints/find)
* **count**: [endpoints/count](endpoints/count)

as well as two actions which aid in publication:

* **partition**: [endpoints/partition](endpoints/partition)
* **publish**: [endpoints/publish](endpoints/publish)

All API requests are done in a two-stage approach by first sending an
Arrow Flight descriptor to the server, returning back a Flight info object
which contains the request and the server to contact, contained within
a Flight ticket. This ticket is then sent to receive back the expected
payload with a specific Arrow flight schema dependent on the request,
serialized in the Arrow 
![streaming format](https://arrow.apache.org/docs/format/Columnar.html#ipc-streaming-format).

The Flight descriptors sent to the server in the first stage are all
specified here as JSON packets which are UTF-8-encoded, using the command
variant of the Flight descriptor, which can be used to specify any
application-specific command.

The Flight descriptor schemas are described within each endpoint in
`descriptor.json`, while the payload schemas are described via `schema.txt`. In
addition, a generic descriptor specification for all endpoints is described in
`endpoints/descriptor.json`.

## Publication

Publication is done by first registering a publisher via the **publish**
endpoint with a publisher ID. If authorized to do so, the server will send a
response with connection details to connect via Kafka to publish data.

The data is published via Kafka with the schema described in
[publication/schema.txt](publication/schema.txt).


## Usage

### Python

The generic Flight descriptor schema is described within each endpoint in
`{endpoint}.json`. In addition, a generic descriptor specification for all
endpoints is described in `descriptor.json`.


```python

from arrakis_schema import load_schema

schema = load_schema("count.json")

```
