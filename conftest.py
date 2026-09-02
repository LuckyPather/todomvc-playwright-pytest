import pytest
from playwright.sync_api import Page

from pages.todo_page import TodoPage
from tests.seeds import SeededTodos


@pytest.fixture
def todo_page(page: Page) -> TodoPage:
    """A ``TodoPage`` opened on a clean application state.

    pytest-playwright gives every test a fresh browser context, but the
    application persists todos in localStorage, so it is cleared explicitly
    rather than relying on context isolation.
    """
    todo = TodoPage(page)
    todo.open()
    todo.clear_storage()
    return todo


@pytest.fixture
def seeded_todos(todo_page: TodoPage) -> SeededTodos:
    """A clean page pre-filled with three todos, one of them completed."""
    return SeededTodos.seed(todo_page)
