from __future__ import annotations

import logging
import multiprocessing.pool
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Union

from domain import commands, events
from service_player import exceptions

if TYPE_CHECKING:
    from . import unit_of_work

logger = logging.getLogger(__name__)

Message = Union[commands.Command, events.Event]


class MessageBus:
    """
    A message bus that handles messages, which can be either events or commands.

    Args:
        uow (unit_of_work.AbstractUnitOfWork): The unit of work to \
use for handling messages.
        event_handlers (Dict[events.Event, list[Callable]]): A dictionary mapping \
events to their handlers.
        command_handlers (Dict[commands.Command, Callable]): A dictionary mapping \
commands to their handlers.
        background_threads (int, optional): The number of background threads \
to use for handling messages. Defaults to 1.
    """

    def __init__(
        self,
        uow: unit_of_work.AbstractUnitOfWork,
        event_handlers: Dict[events.Event, list[Callable]],
        command_handlers: Dict[commands.Command, Callable],
        background_threads: int = 1,
    ):
        """
        Initialize message bus

        Args:
            uow (unit_of_work.AbstractUnitOfWork): _description_
            event_handlers (Dict[events.Event, list[Callable]]): _description_
            command_handlers (Dict[commands.Command, Callable]): _description_
            background_threads (int, optional): _description_. Defaults to 1.
        """

        self.uow: unit_of_work.AbstractUnitOfWork = uow
        self.event_handlers: Dict[events.Event, list[Callable]] = event_handlers
        self.command_handlers: Dict[commands.Command, Callable] = command_handlers
        self.pool = multiprocessing.pool.ThreadPool(background_threads)

    def handle(self, message: Message) -> multiprocessing.pool.AsyncResult:
        """
        Handle message

        Args:
            message (Message): Message to handle. It can be either Event or Command

        Raises:
            ValueError: If message is not Event or Command
        """

        return self.pool.apply_async(self._handle, (message,))

    def _collect_new_events(self) -> None:
        """
        Collect all new events from all instances in the repository
        """

        for event in self.uow.collect_new_events():
            self.handle(event)

    def _handle(self, message: Message) -> Any:
        """
        Handle message

        Args:
            message (Message): Message to handle. It can be either Event or Command

        Returns:
            Any: Result of handling message
        """

        result = None
        for handler in self._get_handlers(message):
            result = handler(message)

        self.pool.apply_async(self._collect_new_events)

        if isinstance(message, commands.Command):
            return result

    def _get_handlers(self, message: Message) -> list[Callable]:
        """
        Get handlers for message

        Args:
            message (Message): Message to get handlers for

        Raises:
            ValueError: If message is not Event or Command

        Returns:
            list[Callable]: List of handlers
        """

        if isinstance(message, commands.Command):
            return self._get_command_handlers(message)
        elif isinstance(message, events.Event):
            return self._get_event_handlers(message)

        raise ValueError(f"Unexpected message {message}")

    def _get_command_handlers(self, command: commands.Command) -> List[Callable]:
        """
        Get command handlers for command

        Args:
            command (commands.Command): Command to get handlers for

        Returns:
            List[Callable]: List of handlers
        """

        return [self.command_handlers[type(command)]]

    def _get_event_handlers(self, event: events.Event) -> List[Callable]:
        """
        Get event handlers for event

        Args:
            event (events.Event): Event to get handlers for

        Returns:
            List[Callable]: List of handlers
        """
        return self.event_handlers[type(event)]

    def _try_process(self, func: Callable) -> Any:
        """
        Try to process function and catch exceptions

        Args:
            func (Callable): Function to process

        Returns:
            Any: Result of processing function
        """

        try:
            return func()
        except exceptions.InternalException as e:
            logger.debug(
                f"Exception processing {func}"
            )  # Do not log internal exceptions as they are expected
            return e
        except Exception as e:
            logger.exception(f"Exception processing {func}")  # Log other exceptions
            return e
