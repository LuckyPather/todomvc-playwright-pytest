"""Deleting a todo item removes it from every view."""

import re

import pytest
from playwright.sync_api import expect

VIEWS = [("All", r"#/$"), ("Active", r"#/active$"), ("Completed", r"#/completed$")]


@pytest.mark.parametrize("completed", [False, True], ids=["active-item", "completed-item"])
def test_deleted_item_disappears_from_every_view(todo_page, completed):
    todo_page.add_todos("Keep this task", "Delete this task")
    if completed:
        todo_page.mark_completed("Delete this task")

    todo_page.delete("Delete this task")

    for view, url_pattern in VIEWS:
        todo_page.filter_by(view)
        expect(todo_page.page).to_have_url(re.compile(url_pattern))
        expect(todo_page.item("Delete this task")).to_have_count(0)

    todo_page.filter_by("All")
    expect(todo_page.todo_titles).to_have_text(["Keep this task"])
