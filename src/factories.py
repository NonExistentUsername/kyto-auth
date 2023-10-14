from typing import Callable, List

import di
from adapters import repository
from domain import commands, events
from service_player import handlers, messagebus, unit_of_work


def create_uow(uow_type: str) -> unit_of_work.AbstractUnitOfWork:
    if uow_type == "ram":
        return unit_of_work.InMemoryUnitOfWork(
            repository.InMemoryRepository(query_fields=["id", "username", "email"])
        )

    raise ValueError(f"Unknown uow_type: {uow_type}")


def create_message_bus(
    uow: unit_of_work.AbstractUnitOfWork,
    event_handlers: dict[events.Event, List[Callable]] = handlers.EVENT_HANDLERS,
    command_handlers: dict[commands.Command, Callable] = handlers.COMMAND_HANDLERS,
) -> messagebus.MessageBus:
    """
    Create message bus

    Args:
        uow (unit_of_work.AbstractUnitOfWork): Unit of work

    Returns:
        messagebus.MessageBus: Message bus
    """

    dependencies = {
        "uow": uow,
    }

    injected_command_handlers = {
        command: di.inject_dependencies(handler, dependencies)
        for command, handler in command_handlers.items()
    }
    injected_event_handlers = {
        event: [
            di.inject_dependencies(handler, dependencies) for handler in handlers_list
        ]
        for event, handlers_list in event_handlers.items()
    }

    return messagebus.MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )
