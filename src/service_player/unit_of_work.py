from __future__ import annotations

import abc
import logging
from copy import deepcopy
from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from src.adapters import repository

logger = logging.getLogger(__name__)


class AbstractUnitOfWork(abc.ABC):
    """
    Abstract class for Unit of Work
    """

    users: repository.AbstractRepository

    def __init__(
        self,
        users: repository.AbstractRepository,
    ):
        """
        Initialize Unit of Work

        Args:
            repositories (repository.AbstractRepository): Users repository
        """

        self.users = users

    def __enter__(self) -> AbstractUnitOfWork:
        """
        Enter Unit of Work

        Returns:
            AbstractUnitOfWork: Unit of Work
        """

        return self

    def __exit__(self, *args):
        """
        Exit Unit of Work
        """

        self.rollback()

    def commit(self):
        """
        Commit all changes made in this unit of work
        """

        self._commit()

    def collect_new_events(self):
        """
        Collect all new events from all instances in the repository

        Yields:
            Event: New event
        """

        for instance in self.users.seen:
            if hasattr(instance, "events") and isinstance(instance.events, list):
                while instance.events:
                    yield instance.events.pop(0)

    @abc.abstractmethod
    def _commit(self):
        """
        Commit all changes made in this unit of work

        Raises:
            NotImplementedError: Not implemented
        """

        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        """
        Rollback all changes made in this unit of work

        Raises:
            NotImplementedError: Not implemented
        """

        raise NotImplementedError


class InMemoryUnitOfWork(AbstractUnitOfWork):
    """
    Unit of Work that stores all changes in RAM
    """

    def __init__(
        self,
        users: repository.AbstractRepository,
    ):
        """
        Initialize InMemoryUnitOfWork

        Args:
            users (repository.AbstractRepository): Users repository
        """

        super().__init__(users)

        self._last_committed_users = deepcopy(users)

    def _commit(self):
        """
        Commit all changes made in this unit of work
        """

        logger.debug("Commiting changes in InMemoryUnitOfWork")

        self._last_committed_users = deepcopy(self.users)

    def rollback(self):
        """
        Rollback all changes made in this unit of work
        """

        logger.debug("Rolling back changes in InMemoryUnitOfWork")

        self.users = deepcopy(self._last_committed_users)
