from __future__ import annotations

import abc
from copy import deepcopy
from typing import Dict, Generic, List, Optional, TypeVar

from domain.base import BaseModel

_T = TypeVar("_T", bound=BaseModel)


class AbstractRepository(abc.ABC, Generic[_T]):
    """
    Abstract base class for repositories.

    Defines the interface for adding and retrieving instances from a repository.
    """

    def __init__(self):
        """
        Initializes a new instance of the AbstractRepository class.
        """

        self.seen: set[_T] = set()

    def add(self, instance: _T) -> None:
        """
        Add instance to repository

        Args:
            instance (_T): Instance
        """

        self._add(instance)
        self.seen.add(instance)

    def get(self, **kwargs) -> Optional[_T]:
        """
        Get instance from repository by keyword arguments

        Raises:
            NotImplementedError: Not implemented

        Returns:
            Optional[_T]: Instance or None if not found
        """

        instance: Optional[_T] = self._get(**kwargs)

        if instance:
            self.seen.add(instance)

        return instance

    def delete(self, **kwargs) -> None:
        instance: Optional[_T] = self._delete(**kwargs)

        if instance:
            self.seen.add(instance)

        return instance

    @abc.abstractmethod
    def _add(self, instance: _T) -> None:
        """
        Add instance to repository

        Args:
            instance (_T): Instance

        Raises:
            NotImplementedError: Not implemented
        """

        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, **kwargs) -> Optional[_T]:
        """
        Get instance from repository by keyword arguments

        Raises:
            NotImplementedError: Not implemented

        Returns:
            Optional[_T]: Instance or None if not found
        """

        raise NotImplementedError

    @abc.abstractmethod
    def _delete(self, **kwargs) -> Optional[_T]:
        """
        Delete instance from repository by keyword arguments

        Raises:
            NotImplementedError: Not implemented

        Returns:
            Optional[_T]: Instance or None if not found
        """

        raise NotImplementedError


class RamRepository(AbstractRepository[_T]):
    """
    In-memory repository implementation that stores instances of a given type \
in a dictionary-like structure.
    The repository can be queried by specifying one or more fields and \
their corresponding values.
    """

    def __init__(
        self,
        query_fields: Optional[List[str]] = None,
    ):
        """
        Initializes a new instance of the RamRepository class.

        Args:
            fields (Optional[List[str]], optional): Fields to query by. \
Defaults to None.
            storages (Optional[Dict[str, Dict[str, _T]]], optional): Storage \
for fields. Defaults to None.
        """

        super().__init__()
        self._query_fields: List[str] = query_fields or []
        self._storages: Dict[str, Dict[str, _T]] = {}

        for field in self._query_fields:
            if field not in self._storages:
                self._storages[field] = {}

    def copy(self) -> RamRepository[_T]:
        """
        Copy repository

        Returns:
            RamRepository: Copy of repository
        """

        fields = self._query_fields.copy()
        storages = deepcopy(self._storages)
        repository = RamRepository(fields, storages)
        repository.seen = self.seen.copy()
        return repository

    def __len__(self) -> int:  # For testing purposes
        """
        Get number of instances in repository

        Returns:
            int: Number of instances in repository
        """

        return len(self._storages[self._query_fields[0]])

    def _add(self, instance: _T) -> None:
        """
        Add instance to repository

        Args:
            instance (_T): Instance
        """

        for field in self._query_fields:
            value = getattr(instance, field)
            self._storages[field][value] = instance

    def _get(self, **kwargs) -> Optional[_T]:
        """
        Get instance from repository by keyword arguments

        Returns:
            Optional[_T]: Instance or None if not found
        """

        for field in self._query_fields:
            if value := kwargs.get(field, None):
                return self._storages[field].get(value, None)

        return None

    def _delete(self, **kwargs) -> Optional[_T]:
        """
        Delete instance from repository by keyword arguments

        Returns:
            Optional[_T]: Instance or None if not found
        """

        instance: Optional[_T] = self._get(**kwargs)

        if instance:
            for field in self._query_fields:
                value = getattr(instance, field)
                del self._storages[field][value]

        return instance
