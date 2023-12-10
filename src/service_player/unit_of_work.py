from __future__ import annotations

import logging
from copy import deepcopy
from typing import TYPE_CHECKING

from kytool.service_player.unit_of_work import AbstractUnitOfWork

if TYPE_CHECKING:
    from kytool.adapters import repository

logger = logging.getLogger(__name__)


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
