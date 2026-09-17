from faststream.rabbit import RabbitBroker
from core import conf

rabbit_broker = RabbitBroker(conf.rabbit.url)