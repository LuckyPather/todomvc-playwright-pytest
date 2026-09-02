"""Shared test data and helpers."""

from dataclasses import dataclass

from pages.todo_page import TodoPage


def items_left(count: int) -> str:
    """The footer counter text the application shows for ``count`` active items."""
    return f"{count} item left" if count == 1 else f"{count} items left"


@dataclass(frozen=True)
class SeededTodos:
    """Todos present on the page after seeding, in insertion order.

    ``completed`` items have been marked as completed; ``active`` items have not.
    """

    page: TodoPage
    all: tuple[str, ...] = ("Walk the dog", "Pay the bills", "Water the plants")
    completed: tuple[str, ...] = ("Pay the bills",)

    @property
    def active(self) -> tuple[str, ...]:
        return tuple(text for text in self.all if text not in self.completed)

    @classmethod
    def seed(cls, page: TodoPage) -> "SeededTodos":
        seeded = cls(page)
        page.add_todos(*seeded.all)
        for text in seeded.completed:
            page.mark_completed(text)
        return seeded
