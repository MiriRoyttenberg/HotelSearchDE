from kafka import KafkaProducer
import requests
import json
import time
import Configuration as c

def request_location(loc):
    response = requests.request("GET", c.url_search_location, headers=c.headers, params= {"locale": "en-gb", "name": loc})

    try:
        dest_id_arr = []
        json_response = json.loads(response.text)
        if len(json_response) != 0:
            for row in range(len(json_response)):
                dest_id = (json_response[row]['dest_id'])
                dest_id_arr.append(dest_id)
                return (dest_id_arr)
        else:
            return 0
    except:
        return ("There is no result for this city name")

def request_hotels(dest_id_arr,room_number,checkin_date,checkout_date,adult_number,user_id,chat_id):
    for row in dest_id_arr:
        querystring1 = {"room_number": room_number, "checkin_date": checkin_date, "checkout_date": checkout_date, "units": "metric",
                        "order_by": "popularity", "adults_number": adult_number, "filter_by_currency": "ILS", "locale": "en-gb",
                        "dest_id": row, "dest_type": "city", "currency_code": "ILS", "currency": "ILS"}

        try:
            response1 = requests.get(url=c.url_search_hotels, headers=c.headers, params=querystring1)
            json_response1 = json.loads(response1.text)
            booking_url = []
            for row1 in range(len(json_response1['result'])):
                print(json_response1['result'][row1])
                row_h = json_response1['result'][row1]
                usr = {"user_id": user_id, "chat_id": chat_id}
                row_h.update(usr)
                booking_url.append(json_response1['result'][row1]['url'])
                time.sleep(1)
                producer = KafkaProducer(bootstrap_servers=c.bootstrapServers)
                producer.send(topic=c.topic1, value=json.dumps(row_h).encode('utf-8'))
                producer.send(topic=c.topic2, value=json.dumps(row_h).encode('utf-8'))
            print(booking_url)
            return booking_url
        except:
            return ("There is no result for this parameters")
    response1 = requests.get(url=c.url_search_hotels, headers=c.headers, params=querystring1)
    json_response1 = json.loads(response1.text)
    for row1 in range(len(json_response1['result'])):
        print(json_response1['result'][row1])
        row_h = json_response1['result'][row1]
        time.sleep(1)
        producer = KafkaProducer(bootstrap_servers=c.bootstrapServers)
        producer.send(topic=c.topic1, value=json.dumps(row_h).encode('utf-8'))
        producer.send(topic=c.topic2, value=json.dumps(row_h).encode('utf-8'))
