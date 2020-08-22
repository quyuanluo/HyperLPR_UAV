#!-*-encoding:utf-8-*-

"""
flask 实现的网络rest api
"""
import redis
import random
import logging

from flask import Flask, redirect

pool = redis.ConnectionPool(host='10.0.0.214',
                                port=5000, db=5,)
rcon = redis.StrictRedis(connection_pool=pool)

prodcons_queue = 'task:prodcons:queue'
pubsub_channel = 'task:pubsub:channel'

app = Flask(__name__)

@app.route('/')
def index():
    html = """
    <br>
    <center><h3>Redis Message Queue</h3>
    <br>
    <a href="/prodcons">生产消费者模式</a>
    <br>
    <br>
    <a href="/pubsub">发布订阅者模式</a>
    </center>
    """
    return html

@app.route('/prodcons')
def prodcons():
    elem = random.randrange(10)
    rcon.lpush(prodcons_queue, elem)
    logging.info("lpush {} -- {}".format(prodcons_queue, elem))
    return redirect('/')

@app.route('/pubsub')
def pubsub():
    ps = rcon.pubsub()
    ps.subscribe(pubsub_channel)
    elem = random.randrange(10)
    rcon.publish(pubsub_channel, elem)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)