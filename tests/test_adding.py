"""Adding new todo items: English text, non-English characters, numbers."""

import pytest
from playwright.sync_api import expect

ADD_CASES = [
    pytest.param("Buy groceries for the week", id="english-text"),
    pytest.param("Купить продукты на неделю", id="cyrillic"),
    pytest.param("牛乳を買いに行く", id="japanese"),
    pytest.param("Prépare le café, bitte schön, señor", id="diacritics"),
    pytest.param("Plan the team offsite 🌍✈️🎉", id="emoji"),
    pytest.param("Read chapters 4, 5 and 12 before 2030", id="text-with-numbers"),
    pytest.param("1234567890", id="digits-only"),
]


@pytest.mark.parametrize("text", ADD_CASES)
def test_new_todo_item_is_added(todo_page, text):
    todo_page.add_todo(text)

    expect(todo_page.todo_titles).to_have_text([text])
    expect(todo_page.items_left_counter).to_have_text("1 item left")
    expect(todo_page.new_todo_input).to_be_empty()
