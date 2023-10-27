import contextlib

import pytest

from src.adapters import repository
from src.service_player import unit_of_work


class SampleObject:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"SampleObject(id={self.id}, name={self.name})"

    def __eq__(self, __value: object) -> bool:
        return (
            isinstance(__value, SampleObject)
            and self.id == __value.id
            and self.name == __value.name
        )

    def __hash__(self) -> int:
        return hash(self.id)


@pytest.fixture
def uow() -> unit_of_work.AbstractUnitOfWork:
    return unit_of_work.InMemoryUnitOfWork(
        users=repository.InMemoryRepository(query_fields=["id"]),
    )


class TestRamUOWCreation:
    def test_works(self, uow: unit_of_work.AbstractUnitOfWork):
        with uow:
            uow.users.add(SampleObject(id="123", name="test"))
            uow.commit()

        assert uow.users.get(id="123") == SampleObject(id="123", name="test")

        with uow:
            instance = uow.users.delete(id="123")
            uow.commit()

            assert instance == SampleObject(id="123", name="test")

        assert uow.users.get(id="123") is None

    def test_rolls_back(self, uow: unit_of_work.AbstractUnitOfWork):
        with uow:
            uow.users.add(SampleObject(id="123", name="test"))

        assert uow.users.get(id="123") is None

    def test_rolls_back_if_exception(self, uow: unit_of_work.AbstractUnitOfWork):
        with contextlib.suppress(Exception):
            with uow:
                uow.users.add(SampleObject(id="123", name="test"))
                raise Exception()

        assert uow.users.get(id="123") is None
