# Moogsoft Alert Translator middleware for Yugabyte Anywhere

Simple Python script that takes default Platform and Universe alerts and converts them into a Moogsoft expected format.

---
Designed to run in a container, so geared towards using environment variables.

## Usage

Build and run Docker container with specified variables or envfile:
```
docker build .
docker run -p 8000:8000 --env-file some_envfile c9d58ddb36ff
```

For testing it's recommended to create a Python venv:
```
python3 -m venv /path/to/new/virtual/environment
```
Install requirements:
```
pip3 install flask requests
```
Export required environment variables and start the server using `python3 mgshook.py`

After the server has started, it's `ip:port/webhook` can be configured as an alert destination in Yugabyte Anywhere.

### Required variables

 - `MGS_URL` :               Moogsoft webhook URL;

 - `MGS_USER` :              Moogsoft account name;

 - `MGS_APIKEY` :            Moogsoft API integration key.


#### Available optional variables

- `MGS_ENABLE_EMPTY` :      Set to "yes" to enable sending empty JSON fields for unset variables;

- `MGS_CERT_PATH` :         Path to CA bundle to verify Moogsoft connection.

- `MGS_AGENT_LOCATION`

- `MGS_EVENT_MGR`

- `MGS_CI_OWNER`            

- `MGS_IROPQ`

- `MGS_UAID`
