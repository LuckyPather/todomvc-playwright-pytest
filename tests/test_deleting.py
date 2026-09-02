"""Deleting a todo item removes it from every view."""

import re

import allure
import pytest
from playwright.sync_api import expect

from pages.todo_page import FILTER_ROUTES, TodoPage
from tests.const import SEEDED_TODOS

pytestmark = [pytest.mark.deleting, allure.feature("Todo list"), allure.story("Deleting items")]

# Item to delete from the seeded list and the counter text expected afterwards.
DELETE_CASES = [
    pytest.param("Walk the dog", "1 item left", id="active-item", marks=pytest.mark.smoke),
    pytest.param("Pay the bills", "2 items left", id="completed-item"),
]


@allure.id("DELETE-1")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.covers("R5")
@pytest.mark.parametrize(("target", "counter"), DELETE_CASES)
def test_deleted_item_disappears_from_every_view(
    seeded_todos: TodoPage, target: str, counter: str, case_id: str
) -> None:
    """A deleted item is absent from the All, Active and Completed views; the rest remain."""
    allure.dynamic.title(f"A deleted item disappears from every view: {case_id}")
    remaining = [text for text in SEEDED_TODOS if text != target]

    seeded_todos.delete(target)

    with allure.step("The counter reflects the remaining active items"):
        expect(seeded_todos.items_left_counter).to_have_text(counter)

    for view, route in FILTER_ROUTES.items():
        seeded_todos.filter_by(view)
        with allure.step(f'The deleted item is absent from the "{view}" view'):
            expect(seeded_todos.page).to_have_url(re.compile(route))
            expect(seeded_todos.item(target)).to_have_count(0)

    seeded_todos.filter_by("All")
    with allure.step("The other items are still listed in their original order"):
        expect(seeded_todos.todo_titles).to_have_text(remaining)


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
