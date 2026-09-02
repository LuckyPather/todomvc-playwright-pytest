"""Functional requirements covered by the suite, linked from the tests into the Allure report."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

import allure

REQUIREMENTS_DOC = (
    "https://github.com/LuckyPather/todomvc-playwright-pytest/blob/main/docs/requirements.md"
)

F = TypeVar("F", bound=Callable)


@dataclass(frozen=True)
class Requirement:
    number: int
    title: str

    @property
    def id(self) -> str:
        return f"R{self.number}"

    @property
    def url(self) -> str:
        return f"{REQUIREMENTS_DOC}#{self.id.lower()}"


R1 = Requirement(1, "A new todo item can be added using English text")
R2 = Requirement(2, "A new todo item can be added using non-English characters")
R3 = Requirement(3, "A new todo item can be added that includes numbers")
R4 = Requirement(4, 'A todo item can be marked as completed and appears in the "Completed" view')
R5 = Requirement(5, "A todo item can be deleted and no longer appears in any view")
R6 = Requirement(6, 'The "Active" filter shows only items that are not completed')
R7 = Requirement(7, 'The "Completed" filter shows only items that have been marked as completed')


def covers(*requirements: Requirement) -> Callable[[F], F]:
    """Attach the requirements a test verifies as links in the Allure report."""

    def decorator(test: F) -> F:
        for requirement in reversed(requirements):
            test = allure.link(
                requirement.url,
                name=f"{requirement.id}: {requirement.title}",
                link_type="requirement",
            )(test)
        return test

    return decorator
