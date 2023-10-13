from __future__ import annotations

import abc
import logging
from copy import deepcopy
from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from adapters import repository

logger = logging.getLogger(__name__)


class AbstractUnitOfWork(abc.ABC):
    """
    Abstract class for Unit of Work
    """

    def __init__(
        self,
        repositories: Dict[str, repository.AbstractRepository],
    ):
        """
        Initialize Unit of Work

        Args:
            repositories (Dict[str, repository.AbstractRepository]): Repositories
        """

        self._repositories = repositories

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

        for _repository in self._repositories.values():
            for instance in _repository.seen:
                if hasattr(instance, "events") and isinstance(instance.events, list):
                    while instance.events:
                        yield instance.events.pop(0)

    def __getattribute__(self, __name: str) -> Any:
        """
        Get attribute from Unit of Work

        Args:
            __name (str): Attribute name

        Returns:
            Any: Attribute value
        """

        try:
            return super().__getattribute__(__name)
        except AttributeError:
            pass

        repository = self._repositories.get(__name)

        if repository is not None:
            return repository

        raise AttributeError(f"Attribute {__name} not found in Unit of Work")

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


class RamUnitOfWork(AbstractUnitOfWork):
    """
    Unit of Work that stores all changes in RAM
    """

    def __init__(
        self,
        repositories: Dict[str, repository.AbstractRepository],
    ):
        """
        Initialize RamUnitOfWork

        Args:
            repositories (Dict[str, repository.AbstractRepository]): Repositories
        """

        super().__init__(repositories)

        self._last_committed_repositories = deepcopy(repositories)

    def _commit(self):
        """
        Commit all changes made in this unit of work
        """

        logger.debug("Commiting changes in RamUnitOfWork")

        self._last_committed_repositories = deepcopy(self._repositories)

    def rollback(self):
        """
        Rollback all changes made in this unit of work
        """

        logger.debug("Rolling back changes in RamUnitOfWork")

        self._repositories = deepcopy(self._last_committed_repositories)
