from kytool.adapters import repository
from kytool.factories import create_message_bus, create_uow
from kytool.service_player.messagebus import MessageBus

from src.service_player import unit_of_work

# Its required to import all handlers here
from src.service_player.handlers import *

message_bus = create_message_bus(
    unit_of_work.InMemoryUnitOfWork(
        repository.InMemoryRepository(query_fields=["id", "username", "email"])
    ),
    background_threads=2,
)


async def get_message_bus() -> MessageBus:
    return message_bus
