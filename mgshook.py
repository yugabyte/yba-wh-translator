# app.py

# Simple webhook gateway which listens for a webhook from yugabyte anywhere and
# reformats and sends it to moogsoft in desired format

from flask import Flask, request

import json, requests, os
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

if not (os.getenv('MGS_URL')):
    print("\nMoogsoft URL is missing! Please set MGS_URL env var.")
    exit()
if not (os.getenv('MGS_USER')):
    print("\nMoogsoft username is missing! Please set MGS_USER env var.")
    exit()
if not (os.getenv('MGS_APIKEY')):
    print("\nMoogsoft API key is missing! Please set MGS_APIKEY env var.")
    exit()

destUrl = os.getenv('MGS_URL')
username = os.getenv('MGS_USER')
apiKey = os.getenv('MGS_APIKEY')

custom_agent_location = os.getenv('MGS_AGENT_LOCATION')
custom_event_manager = os.getenv('MGS_EVENT_MGR')
custom_ciowner = os.getenv('MGS_CI_OWNER')
custom_iropqueue = os.getenv('MGS_IROPQ')
custom_uaid = os.getenv('MGS_UAID')
emptyvars = os.getenv('MGS_ENABLE_EMPTY')
certificate = os.getenv('MGS_CERT_PATH')


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        print("\nData received from Webhook is: ")
        jsonFmt = json.dumps( request.json, indent=4 )
        print( jsonFmt )
        #check if alert is universe-related vs platform
        if request.json['alerts'][0]['labels']['configuration_type'] == "UNIVERSE":
            data = {}
            #data['signature'] = 'custom_alert_priority'
            data['source'] = request.json['alerts'][0]['labels']['universe_name']
            data['source_id'] = request.json['alerts'][0]['labels']['universe_uuid']
            data['external_id'] = request.json['alerts'][0]['labels']['definition_uuid']
            if custom_agent_location or emptyvars:
                data['agent_location'] = custom_agent_location
            #severity mapping
            if request.json['alerts'][0]['labels']['severity'].lower() == "severe":
                data['severity'] = "5"
            elif request.json['alerts'][0]['labels']['severity'].lower() == "warning":
                data['severity'] = "3"
            data['type'] = request.json['alerts'][0]['labels']['alertname']
            if custom_event_manager or emptyvars:
                data['manager'] = custom_event_manager
            data['class'] = 'Database'
            data['description'] = request.json['alerts'][0]['annotations']['message']
            data['agent'] = 'Yugabyte'
            data['agent_time'] = request.json['alerts'][0]['startsAt']
            data['event_time'] = request.json['alerts'][0]['startsAt']
            if custom_ciowner or emptyvars:
                data['ciowner'] = custom_ciowner
            if custom_iropqueue or emptyvars:
                data['iropqueue'] = custom_iropqueue
            if custom_uaid or emptyvars:
                data['uaid'] = custom_uaid
            data['metric_value'] = request.json['alerts'][0]['labels']['threshold']
            data['metric_thresdhold'] = request.json['alerts'][0]['labels']['threshold']

            jsonSend = json.dumps( data, indent = 4 )

        else: #platform alert
            data = {}
            #data['signature'] = 'custom_alert_priority'
            data['source'] = "platform_customer_" + request.json['alerts'][0]['labels']['customer_uuid']
            data['source_id'] = request.json['alerts'][0]['labels']['customer_uuid']
            data['external_id'] = request.json['alerts'][0]['labels']['definition_uuid']
            if custom_agent_location or emptyvars:
                data['agent_location'] = custom_agent_location
            #severity mapping
            if request.json['alerts'][0]['labels']['severity'].lower() == "severe":
                data['severity'] = "5"
            elif request.json['alerts'][0]['labels']['severity'].lower() == "warning":
                data['severity'] = "3"
            data['type'] = request.json['alerts'][0]['labels']['alertname']
            if custom_event_manager or emptyvars:
                data['manager'] = custom_event_manager
            data['class'] = 'Database'
            data['description'] = request.json['alerts'][0]['annotations']['message']
            data['agent'] = 'Yugabyte'
            data['agent_time'] = request.json['alerts'][0]['startsAt']
            data['event_time'] = request.json['alerts'][0]['startsAt']
            if custom_ciowner or emptyvars:
                data['ciowner'] = custom_ciowner
            if custom_iropqueue or emptyvars:
                data['iropqueue'] = custom_iropqueue
            if custom_uaid or emptyvars:
                data['uaid'] = custom_uaid
            data['metric_value'] = request.json['alerts'][0]['labels']['threshold']
            data['metric_thresdhold'] = request.json['alerts'][0]['labels']['threshold']

            jsonSend = json.dumps( data, indent = 4 )

        print("\nData to send to Moogsoft is: ")
        print( jsonSend )
        auth = HTTPBasicAuth(username, apiKey)
        if certificate:
            rsp = requests.post(destUrl, data=jsonSend, headers={'Content-Type': 'application/json'}, auth=auth, verify=certificate)
        else:
            rsp = requests.post(destUrl, data=jsonSend, headers={'Content-Type': 'application/json'}, auth=auth, verify=True)
        return "Webhook received!"


app.run(host='0.0.0.0', port=8000)
