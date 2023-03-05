# flask-event-propagator
This service periodically sends a predefined JSON object to a specific HTTP API endpoint every N seconds.

# Configuration
The service can be configured through a configuration file (config.json). 
Here are the available configuration options:

* wait_time: The time interval between sending JSON objects (events) in seconds.
* requests_endpoint: The HTTP API endpoint that the payloads will be sent to.
* events_file: The location of the file containing the predefined JSON objects (events) that can be sent.

# Installation
```sh
git clone 
```
