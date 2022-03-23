# Use this file to setup the database consumer that stores the ride information in the database
import pika
import sys
import os
import json
import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client.consumerdb
collection = db.consumers

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='database')

    def callback(ch, method, properties, body):
        body = body.decode('utf8').replace("'", '"')
        body = json.loads(body)
        print(" [x] Received %r" % body)
        collection.insert_one({'cid':body['consumerid'],'ip':body['ipaddr']})
        
        ##DEBUG
        print("inserted into db")
        for item in collection.find():
            print(item)


        
    channel.basic_consume(queue='database', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
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