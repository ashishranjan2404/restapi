# import os
# import logging
# from kafka import KafkaProducer
# from kafka import KafkaConsumer
# from typing import Dict
#
# # Export exception class
# logger = logging.getLogger(__name__)
#
# P1_TOPIC = "p1"
# P2_TOPIC = "p2"
# P3_TOPIC = "p3"
#
#
# class Consumer:
#     def __init__(self, bootstrap_server, topic):
#         logging.info('Kafka consumer starting on topics {}.')
#         self._consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_server,group_id="webapi")
#         self._partitions = self._consumer.partitions_for_topic()
#         self._cancelled = False
#     def close(self):
#         logging.info('Kafka consumer closing...')
#         self._cancelled = True
#         self._consumer.close()
#     def consume(self):
#         return self._consumer.seek_to_beginning(self._partitions)
#
#
# class Producer:
#     def __init__(self, bootstrap_server):
#         logging.info('Kafka producer starting...')
#         self._producer = KafkaProducer(bootstrap_server)
#
#     def produce(self, topic, value, on_delivery=None):
#         self._producer.send(topic=topic,value=value)
#
#
# consumers: Dict = None
#
# producer: Producer = None
#
#
# # def add_consumers():
# #     global consumers
# #     consumers = {}
# #     for TOPIC in [P1_TOPIC, P2_TOPIC, P3_TOPIC]:
# #         consumers[TOPIC] = Consumer(bootstrap_server=os.getenv('KAFKA_URL', '0.0.0.0:32777'),
# #                                     topic=TOPIC)
#
#
# def close():
#     global consumers, producer
#     if producer:
#         producer.close()
#     for consumer in consumers:
#         consumers[consumer].close()
#
#
# def get_producer() -> Producer:
#     global producer
#     return producer
#
#
# def get_consumers():
#     global consumers
#     return consumers
#
#
# def create_producer():
#     global producer
#     producer = Producer(bootstrap_server=os.getenv('KAFKA_URL', '0.0.0.0:32777'))
#
