"""Deleting a todo item removes it from every view."""

import re

import pytest
from playwright.sync_api import expect

from pages.todo_page import FILTER_ROUTES, TodoPage
from tests.seeds import SeededTodos, items_left

pytestmark = pytest.mark.deleting

DELETE_CASES = [
    pytest.param("Walk the dog", id="active-item", marks=pytest.mark.smoke),
    pytest.param("Pay the bills", id="completed-item"),
]


@pytest.mark.parametrize("target", DELETE_CASES)
def test_deleted_item_disappears_from_every_view(seeded_todos: SeededTodos, target: str) -> None:
    todo_page = seeded_todos.page
    remaining = [text for text in seeded_todos.all if text != target]
    remaining_active = [text for text in seeded_todos.active if text != target]

    todo_page.delete(target)

    expect(todo_page.items_left_counter).to_have_text(items_left(len(remaining_active)))
    for view, route in FILTER_ROUTES.items():
        todo_page.filter_by(view)
        expect(todo_page.page).to_have_url(re.compile(route))
        expect(todo_page.item(target)).to_have_count(0)

    todo_page.filter_by("All")
    expect(todo_page.todo_titles).to_have_text(remaining)


@pytest.mark.edge
def test_deleting_the_only_item_leaves_an_empty_list(todo_page: TodoPage) -> None:
    todo_page.add_todo("The only task")

    todo_page.delete("The only task")

    expect(todo_page.todo_items).to_have_count(0)
    expect(todo_page.items_left_counter).to_be_hidden()
