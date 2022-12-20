from kafka import KafkaProducer
import requests
import json
import time
import Configuration as c

response = requests.request("GET", c.url_search_location, headers=c.headers, params=c.querystring_loc)

dest_id_arr = []
json_response = json.loads(response.text)
for row in range(len(json_response)):
    dest_id = (json_response[row]['dest_id'])
    dest_id_arr.append(dest_id)
print(dest_id_arr)

for row in dest_id_arr:
    querystring1 = {"room_number": "1", "checkin_date": "2023-05-27", "checkout_date": "2023-05-28", "units": "metric",
                    "order_by": "popularity", "adults_number": "2", "filter_by_currency": "ILS", "locale": "en-gb",
                    "dest_id": row, "dest_type": "city", "currency_code": "ILS", "currency": "ILS"}

    response1 = requests.get(url=c.url_search_hotels, headers=c.headers, params=querystring1)
    json_response1 = json.loads(response1.text)
    for row1 in range(len(json_response1['result'])):
        print(json_response1['result'][row1])
        row_h = json_response1['result'][row1]
        time.sleep(1)
        producer = KafkaProducer(bootstrap_servers=c.bootstrapServers)
        producer.send(topic=c.topic1, value=json.dumps(row_h).encode('utf-8'))
        producer.send(topic=c.topic2, value=json.dumps(row_h).encode('utf-8'))
