"""Adding new todo items: English text, non-English characters, numbers."""

import re

import pytest
from playwright.sync_api import expect

from pages.todo_page import TodoPage

pytestmark = pytest.mark.adding

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


@pytest.mark.parametrize("text", ADD_CASES)
def test_new_todo_item_is_added(todo_page: TodoPage, text: str) -> None:
    todo_page.add_todo(text)

    expect(todo_page.todo_titles).to_have_text([text])
    expect(todo_page.items_left_counter).to_have_text("1 item left")
    expect(todo_page.new_todo_input).to_be_empty()


@pytest.mark.edge
def test_surrounding_whitespace_is_trimmed(todo_page: TodoPage) -> None:
    todo_page.add_todo("   Trim me   ")

    # Anchored pattern on purpose: plain-string matching normalizes whitespace
    # on both sides and would pass even if the title kept its padding.
    expect(todo_page.todo_titles).to_have_text([re.compile(r"^Trim me$")])
    expect(todo_page.items_left_counter).to_have_text("1 item left")


@pytest.mark.edge
@pytest.mark.parametrize("text", BLANK_CASES)
def test_blank_input_does_not_add_an_item(todo_page: TodoPage, text: str) -> None:
    todo_page.add_todo(text)

    expect(todo_page.todo_items).to_have_count(0)
    expect(todo_page.items_left_counter).to_be_hidden()


@pytest.mark.edge
def test_duplicate_items_are_allowed(todo_page: TodoPage) -> None:
    todo_page.add_todos("Call the dentist", "Call the dentist")

    expect(todo_page.todo_titles).to_have_text(["Call the dentist", "Call the dentist"])
    expect(todo_page.items_left_counter).to_have_text("2 items left")
