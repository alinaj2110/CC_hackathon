# Code for Ride Matching Consumer
import requests
import pika
import sys
import os
import json
from time import sleep

sleep(10)
## TO DELETE LATER
CONSUMER_ID= os.environ['CONSUMER_ID']
PRODUCER_ADDRESS= os.environ['PRODUCER_ADDRESS']

def main():
    init_req = {'consumerid':CONSUMER_ID,'ipaddr':'127.0.0.1:5020'}
    res = requests.post('http://'+PRODUCER_ADDRESS+'/new_ride_matching_consumer', json=init_req)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='ride_match')

    def callback(ch, method, properties, body):
        body = body.decode('utf8').replace("'", '"')
        body = json.loads(body)
        print("\n\n============================================")
        print("Ride Request Received...")
        print("Details of Request:")
        print("\tPickup:",body['pickup'])
        print("\tDestination:",body['destination'])
        print("\tCost:",body['cost'])
        print("\tSeats:",body['seats'])
        print("\nProcessing Request...")
        print('Estimated Time To Process:',body['time'])
        
        sleep(body['time'])

        print("Processing Done...")
        print("Task ID:",body['taskid'])
        print("Consumer ID:",CONSUMER_ID)
        print("============================================\n\n")

        
    channel.basic_consume(queue='ride_match', on_message_callback=callback, auto_ack=True)
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