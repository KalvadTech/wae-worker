#!/usr/bin/env python
import pika
import os
import json
from yeelight import discover_bulbs, Bulb
import time

connection = pika.BlockingConnection(
    parameters=pika.URLParameters(os.getenv("AMQP_URL", "value does not exist"))
)
channel = connection.channel()


def callback(ch, method, properties, body):
    print(" [x] Received %r." % body)
    bulbs = discover_bulbs()
    body_s = body.decode("utf-8")
    print(body)
    print(body_s)
    for bulb_raw in bulbs:
        bulb = Bulb(bulb_raw["ip"])
        bulb.turn_on()
        bulb.set_brightness(100)
        if body_s == "error":
            bulb.set_rgb(255, 0, 0)  # red
        elif body_s == "success":
            bulb.set_rgb(0, 255, 0)  # green
        elif body_s == "statping_error":
            bulb.set_rgb(255, 51, 51)  # red
            time.sleep(1)
            bulb.set_rgb(255, 128, 0)  # orange
            time.sleep(1)
            bulb.set_rgb(255, 51, 51)  # red
        #        else:
        #            bulb.set_rgb(0, 0, 255) #blue
    time.sleep(3)
    for bulb_raw in bulbs:
        bulb = Bulb(bulb_raw["ip"])
        bulb.set_rgb(255, 255, 255)  # white


channel.basic_consume(queue="wae-light", on_message_callback=callback, auto_ack=True)

print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
