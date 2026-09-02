"""Deleting a todo item removes it from every view."""

import re

import allure
import pytest
from playwright.sync_api import expect

from pages.todo_page import FILTER_ROUTES, TodoPage
from tests.seeds import SeededTodos, items_left

pytestmark = [pytest.mark.deleting, allure.feature("Todo list"), allure.story("Deleting items")]

DELETE_CASES = [
    pytest.param("Walk the dog", id="active-item", marks=pytest.mark.smoke),
    pytest.param("Pay the bills", id="completed-item"),
]


@allure.id("DELETE-1")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.covers("R5")
@pytest.mark.parametrize("target", DELETE_CASES)
def test_deleted_item_disappears_from_every_view(
    seeded_todos: SeededTodos, target: str, case_id: str
) -> None:
    """A deleted item is absent from the All, Active and Completed views; the rest remain."""
    allure.dynamic.title(f"A deleted item disappears from every view: {case_id}")
    todo_page = seeded_todos.page
    remaining = [text for text in seeded_todos.all if text != target]
    remaining_active = [text for text in seeded_todos.active if text != target]

    todo_page.delete(target)

    with allure.step("The counter reflects the remaining active items"):
        expect(todo_page.items_left_counter).to_have_text(items_left(len(remaining_active)))

    for view, route in FILTER_ROUTES.items():
        todo_page.filter_by(view)
        with allure.step(f'The deleted item is absent from the "{view}" view'):
            expect(todo_page.page).to_have_url(re.compile(route))
            expect(todo_page.item(target)).to_have_count(0)

    todo_page.filter_by("All")
    with allure.step("The other items are still listed in their original order"):
        expect(todo_page.todo_titles).to_have_text(remaining)


@allure.id("DELETE-2")
@allure.title("Deleting the only item leaves an empty list")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.covers("R5")
@pytest.mark.edge
def test_deleting_the_only_item_leaves_an_empty_list(todo_page: TodoPage) -> None:
    """With the last item gone, the list is empty and the footer with the counter is hidden."""
    todo_page.add_todo("The only task")

    todo_page.delete("The only task")

    with allure.step("The list is empty and the footer is hidden"):
        expect(todo_page.todo_items).to_have_count(0)
        expect(todo_page.items_left_counter).to_be_hidden()
