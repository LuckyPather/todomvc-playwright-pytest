"""Deleting a todo item removes it from every view."""

import re

import pytest
from playwright.sync_api import expect

from pages.todo_page import FILTER_ROUTES, TodoPage

pytestmark = pytest.mark.deleting

DELETE_CASES = [
    pytest.param(False, id="active-item", marks=pytest.mark.smoke),
    pytest.param(True, id="completed-item"),
]


@pytest.mark.parametrize("completed", DELETE_CASES)
def test_deleted_item_disappears_from_every_view(todo_page: TodoPage, completed: bool) -> None:
    todo_page.add_todos("Keep this task", "Delete this task")
    if completed:
        todo_page.mark_completed("Delete this task")

    todo_page.delete("Delete this task")

    expect(todo_page.items_left_counter).to_have_text("1 item left")
    for view, route in FILTER_ROUTES.items():
        todo_page.filter_by(view)
        expect(todo_page.page).to_have_url(re.compile(route))
        expect(todo_page.item("Delete this task")).to_have_count(0)

    todo_page.filter_by("All")
    expect(todo_page.todo_titles).to_have_text(["Keep this task"])
