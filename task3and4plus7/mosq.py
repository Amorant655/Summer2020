import asyncio
from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_1


class MQTTConstants:
    mqtt_address = 'mqtt://mqtt'


class MQTTRuntime:
    mqtt = None

    @classmethod
    def deploy(cls):
        if cls.mqtt is None:
            cls.mqtt = MQTTClient()
            yield from cls.mqtt.connect(MQTTConstants.mqtt_address)


def loop_coroutine(topic, callback):
    yield from MQTTRuntime.deploy()
    yield from MQTTRuntime.mqtt.subscribe([(topic, QOS_1)])
    runnig = True
    while runnig:
        message = yield from MQTTRuntime.mqtt.deliver_message()
        packet = message.publish_packet
        runnig = callback(float(packet.payload.data.decode("utf-8")))
    yield from MQTTRuntime.mqtt.disconnect()


def start_coroutine(topic, callback):
    asyncio.get_event_loop().create_task(loop_coroutine(topic, callback))
