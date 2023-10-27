from src.factories import create_message_bus, create_uow
from src.service_player.messagebus import MessageBus

message_bus = create_message_bus(create_uow("ram"))


async def get_message_bus() -> MessageBus:
    return message_bus
