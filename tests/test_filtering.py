"""The Active and Completed filters show only matching items."""

import re

import allure
import pytest
from playwright.sync_api import expect

from pages.todo_page import FILTER_ROUTES, TodoPage
from tests.seeds import SeededTodos, items_left

pytestmark = [pytest.mark.filtering, allure.feature("Todo list"), allure.story("Filtering")]


@allure.id("FILTER-1")
@allure.title('The "Active" filter shows only active items')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.covers("R6")
@pytest.mark.smoke
def test_active_filter_shows_only_active_items(seeded_todos: SeededTodos) -> None:
    """With a mix of active and completed items, the Active view lists the active ones only."""
    todo_page = seeded_todos.page

    todo_page.filter_by("Active")

    with allure.step("The URL points at the Active view"):
        expect(todo_page.page).to_have_url(re.compile(FILTER_ROUTES["Active"]))
    with allure.step("Only the active items are listed, in insertion order"):
        expect(todo_page.todo_titles).to_have_text(list(seeded_todos.active))
        for text in seeded_todos.completed:
            expect(todo_page.item(text)).to_have_count(0)
    with allure.step("The counter is unaffected by the view"):
        expect(todo_page.items_left_counter).to_have_text(items_left(len(seeded_todos.active)))


@allure.id("FILTER-2")
@allure.title('The "Completed" filter shows only completed items')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.covers("R7")
@pytest.mark.smoke
def test_completed_filter_shows_only_completed_items(seeded_todos: SeededTodos) -> None:
    """With a mix of active and completed items, the Completed view lists only completed ones."""
    todo_page = seeded_todos.page

    todo_page.filter_by("Completed")

    with allure.step("The URL points at the Completed view"):
        expect(todo_page.page).to_have_url(re.compile(FILTER_ROUTES["Completed"]))
    with allure.step("Only the completed items are listed, in insertion order"):
        expect(todo_page.todo_titles).to_have_text(list(seeded_todos.completed))
        for text in seeded_todos.active:
            expect(todo_page.item(text)).to_have_count(0)
    with allure.step("The counter is unaffected by the view"):
        expect(todo_page.items_left_counter).to_have_text(items_left(len(seeded_todos.active)))


@allure.id("FILTER-3")
@allure.title('The "Active" view is empty when every item is completed')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.covers("R6")
@pytest.mark.edge
def test_active_filter_is_empty_when_every_item_is_completed(seeded_todos: SeededTodos) -> None:
    """Once every item is completed, the Active view is empty and the counter reads zero."""
    todo_page = seeded_todos.page
    for text in seeded_todos.active:
        todo_page.mark_completed(text)

    todo_page.filter_by("Active")

    with allure.step("The Active view is empty and the counter reads zero"):
        expect(todo_page.page).to_have_url(re.compile(FILTER_ROUTES["Active"]))
        expect(todo_page.items_left_counter).to_have_text("0 items left")
        expect(todo_page.todo_items).to_have_count(0)


@allure.id("FILTER-4")
@allure.title('The "Completed" view is empty when nothing is completed')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.covers("R7")
@pytest.mark.edge
def test_completed_filter_is_empty_when_nothing_is_completed(todo_page: TodoPage) -> None:
    """Without completed items, the Completed view is empty while the counter still counts."""
    todo_page.add_todos("Walk the dog", "Water the plants")

    todo_page.filter_by("Completed")

    with allure.step("The Completed view is empty and the counter still counts active items"):
        expect(todo_page.page).to_have_url(re.compile(FILTER_ROUTES["Completed"]))
        expect(todo_page.items_left_counter).to_have_text("2 items left")
        expect(todo_page.todo_items).to_have_count(0)
