"""Adding new todo items: English text, non-English characters, numbers."""

import re

import allure
import pytest
from playwright.sync_api import expect

from pages.todo_page import TodoPage
from tests.requirements import R1, R2, R3, covers

pytestmark = [pytest.mark.adding, allure.feature("Todo list"), allure.story("Adding items")]

ADD_CASES = [
    pytest.param("Buy groceries for the week", id="english-text", marks=pytest.mark.smoke),
    pytest.param("Купить продукты на неделю", id="cyrillic"),
    pytest.param("牛乳を買いに行く", id="japanese"),
    pytest.param("شراء الحليب والخبز صباح الغد", id="arabic-rtl"),
    pytest.param("Prépare le café, bitte schön, señor", id="diacritics"),
    pytest.param("Plan the team offsite 🌍✈️🎉", id="emoji"),
    pytest.param("Read chapters 4, 5 and 12 before 2030", id="text-with-numbers"),
    pytest.param("1234567890", id="digits-only"),
    pytest.param("Order 2 pizzas & 3 sodas for $45 (party!)", id="special-characters"),
    pytest.param("a", id="single-character", marks=pytest.mark.edge),
    pytest.param(("lorem ipsum " * 40).strip(), id="long-text", marks=pytest.mark.edge),
    pytest.param(
        "<b>bold</b> & <script>alert(1)</script>", id="html-markup", marks=pytest.mark.edge
    ),
]

BLANK_CASES = [
    pytest.param("", id="empty"),
    pytest.param("   ", id="whitespace-only"),
]


@allure.id("ADD-1")
@allure.severity(allure.severity_level.CRITICAL)
@covers(R1, R2, R3)
@pytest.mark.parametrize("text", ADD_CASES)
def test_new_todo_item_is_added(todo_page: TodoPage, text: str, case_id: str) -> None:
    """A todo item entered in the input field appears in the list with its exact text."""
    allure.dynamic.title(f"A new todo item is added: {case_id}")

    todo_page.add_todo(text)

    with allure.step("The item is listed once with the entered text"):
        expect(todo_page.todo_titles).to_have_text([text])
    with allure.step("The counter shows one item and the input is cleared"):
        expect(todo_page.items_left_counter).to_have_text("1 item left")
        expect(todo_page.new_todo_input).to_be_empty()


@allure.id("ADD-2")
@allure.title("Surrounding whitespace is trimmed from a new item")
@allure.severity(allure.severity_level.NORMAL)
@covers(R1)
@pytest.mark.edge
def test_surrounding_whitespace_is_trimmed(todo_page: TodoPage) -> None:
    """Leading and trailing spaces are not part of the stored item text."""
    todo_page.add_todo("   Trim me   ")

    with allure.step("The item text has no leading or trailing whitespace"):
        # Anchored pattern on purpose: plain-string matching normalizes whitespace
        # on both sides and would pass even if the title kept its padding.
        expect(todo_page.todo_titles).to_have_text([re.compile(r"^Trim me$")])
        expect(todo_page.items_left_counter).to_have_text("1 item left")


@allure.id("ADD-3")
@allure.severity(allure.severity_level.NORMAL)
@covers(R1)
@pytest.mark.edge
@pytest.mark.parametrize("text", BLANK_CASES)
def test_blank_input_does_not_add_an_item(todo_page: TodoPage, text: str, case_id: str) -> None:
    """Confirming an empty or whitespace-only input leaves the list untouched."""
    allure.dynamic.title(f"Blank input does not add an item: {case_id}")

    todo_page.add_todo(text)

    with allure.step("No item is created and the footer stays hidden"):
        expect(todo_page.todo_items).to_have_count(0)
        expect(todo_page.items_left_counter).to_be_hidden()


@allure.id("ADD-4")
@allure.title("Two items with identical text can coexist")
@allure.severity(allure.severity_level.MINOR)
@covers(R1)
@pytest.mark.edge
def test_duplicate_items_are_allowed(todo_page: TodoPage) -> None:
    """The application does not deduplicate items with the same text."""
    todo_page.add_todos("Call the dentist", "Call the dentist")

    with allure.step("Both items are listed and counted"):
        expect(todo_page.todo_titles).to_have_text(["Call the dentist", "Call the dentist"])
        expect(todo_page.items_left_counter).to_have_text("2 items left")
