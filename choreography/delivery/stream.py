from faststream import FastStream
from faststream.kafka import KafkaBroker
from src.config import settings


class TestKafkaBroker(KafkaBroker):
    
    async def publish(self, *args, **kwargs):
        ...


broker = KafkaBroker(settings.broker_url)
#broker = TestKafkaBroker()
app = FastStream(
    broker,
)