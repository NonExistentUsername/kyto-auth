from kytool.factories import create_message_bus, create_uow
from kytool.service_player.messagebus import MessageBus

# Its required to import all handlers here
from src.service_player.handlers import *

message_bus = create_message_bus(create_uow("ram"))


async def get_message_bus() -> MessageBus:
    return message_bus
