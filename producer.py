from flask import Flask, request
from random import randint
import pika
import json
from time import sleep


app = Flask(__name__)

@app.route('/new_ride',methods = ['POST'])
def new_ride():
    if request.method == 'POST':
        postdata = request.data.decode('utf8').replace("'", '"')
        postdata = json.loads(postdata)

        task_id = randint(1,100000)
        postdata['taskid'] = task_id
        message_body = json.dumps(postdata)

        rabbitclient('ride_match','ride_match',message_body)

        return 'Producer received new ride data'

@app.route('/new_ride_matching_consumer',methods = ['POST'])
def new_ride_matching_consumer():
    if request.method == 'POST':
        postdata = request.data.decode('utf8').replace("'", '"')
        
        rabbitclient('database','database',postdata)

        return 'Producer received new ride matching consumer data'

def rabbitclient(rqueue,rrouting_key, rbody):
    connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq'))

    channel = connection.channel()

    channel.queue_declare(queue=rqueue)

    channel.basic_publish(exchange='', routing_key=rrouting_key, body=rbody)
    connection.close()

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000)
