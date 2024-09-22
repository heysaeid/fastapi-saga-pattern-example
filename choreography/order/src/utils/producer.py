from utils.stream import broker


@broker.publisher("create-payment")
async def create_payment(data: dict) -> str:
    return "Hi!"