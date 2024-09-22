from faststream import FastStream
from faststream.kafka import KafkaBroker
from config import settings

broker = KafkaBroker(settings.broker_url)
app = FastStream(broker)


@broker.subscriber("create-payment")
async def handle() -> str:
    return 