# Code for Ride Matching Consumer
import requests
import pika
import sys
import os
import json
from time import sleep

sleep(90)
## TO DELETE LATER
CONSUMER_ID= 124
PRODUCER_ADDRESS= 'http://127.0.0.1:5000/'

init_req = {'consumerid':CONSUMER_ID,'ipaddr':'127.0.0.1:5020'}
res = requests.post(PRODUCER_ADDRESS+'/new_ride_matching_consumer', json=init_req)
print(res.text)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='ride_match')

    def callback(ch, method, properties, body):
        body = body.decode('utf8').replace("'", '"')
        body = json.loads(body)
        print('Time to sleep:',body['time'])
        
        sleep(body['time'])

        print(" [x] Received %r" % body)
        
        print("Task ID:",body['taskid'])
        print("Consumer ID:",CONSUMER_ID)

        
    channel.basic_consume(queue='ride_match', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)