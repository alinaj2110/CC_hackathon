# Use this file to setup the database consumer that stores the ride information in the database
import pika
import sys
import os
import json
import pymongo
from time import sleep

sleep(10)

client = pymongo.MongoClient("mongo", 27017)
db = client.consumerdb
collection = db.consumers

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='database')

    def callback(ch, method, properties, body):
        body = body.decode('utf8').replace("'", '"')
        body = json.loads(body)
        print("\n\n============================================")
        print("Database Received %r" % body)
        print("============================================\n\n",)
        collection.insert_one({'cid':body['consumerid'],'ip':body['ipaddr']})
        
        '''##DEBUG
        print("inserted into db")
        for item in collection.find():
            print(item)
        '''

        
    channel.basic_consume(queue='database', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            client.close()
            sys.exit(0)
        except SystemExit:
            os._exit(0)