"""The Active and Completed filters show only matching items."""

import re

import pytest
from playwright.sync_api import expect

from pages.todo_page import FILTER_ROUTES, TodoPage
from tests.seeds import SeededTodos, items_left

pytestmark = pytest.mark.filtering


@pytest.mark.smoke
def test_active_filter_shows_only_active_items(seeded_todos: SeededTodos) -> None:
    todo_page = seeded_todos.page

    todo_page.filter_by("Active")

    expect(todo_page.page).to_have_url(re.compile(FILTER_ROUTES["Active"]))
    expect(todo_page.todo_titles).to_have_text(list(seeded_todos.active))
    for text in seeded_todos.completed:
        expect(todo_page.item(text)).to_have_count(0)
    expect(todo_page.items_left_counter).to_have_text(items_left(len(seeded_todos.active)))


@pytest.mark.smoke
def test_completed_filter_shows_only_completed_items(seeded_todos: SeededTodos) -> None:
    todo_page = seeded_todos.page

    todo_page.filter_by("Completed")

    expect(todo_page.page).to_have_url(re.compile(FILTER_ROUTES["Completed"]))
    expect(todo_page.todo_titles).to_have_text(list(seeded_todos.completed))
    for text in seeded_todos.active:
        expect(todo_page.item(text)).to_have_count(0)
    expect(todo_page.items_left_counter).to_have_text(items_left(len(seeded_todos.active)))


@pytest.mark.edge
def test_active_filter_is_empty_when_every_item_is_completed(seeded_todos: SeededTodos) -> None:
    todo_page = seeded_todos.page
    for text in seeded_todos.active:
        todo_page.mark_completed(text)

    todo_page.filter_by("Active")

    expect(todo_page.page).to_have_url(re.compile(FILTER_ROUTES["Active"]))
    expect(todo_page.items_left_counter).to_have_text("0 items left")
    expect(todo_page.todo_items).to_have_count(0)


@pytest.mark.edge
def test_completed_filter_is_empty_when_nothing_is_completed(todo_page: TodoPage) -> None:
    todo_page.add_todos("Walk the dog", "Water the plants")

    todo_page.filter_by("Completed")

    expect(todo_page.page).to_have_url(re.compile(FILTER_ROUTES["Completed"]))
    expect(todo_page.items_left_counter).to_have_text("2 items left")
    expect(todo_page.todo_items).to_have_count(0)
