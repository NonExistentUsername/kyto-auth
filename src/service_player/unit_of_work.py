from __future__ import annotations

import logging
from copy import deepcopy
from typing import TYPE_CHECKING

from kytool.service_player import unit_of_work

if TYPE_CHECKING:
    from kytool.adapters import repository

logger = logging.getLogger(__name__)


class AbstractUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self, users: repository.AbstractRepository):
        super().__init__(repositories=dict(users=users))

    @property
    def users(self) -> repository.AbstractRepository:
        """
        Users repository

        Returns:
            repository.AbstractRepository: Users repository
        """

        return self.r("users")


class InMemoryUnitOfWork(AbstractUnitOfWork, unit_of_work.InMemoryUnitOfWork):
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

        super().__init__(users=users)
