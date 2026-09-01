"""The Active and Completed filters show only matching items."""

import re

from playwright.sync_api import expect


def test_active_filter_shows_only_active_items(todo_page):
    todo_page.add_todos("Walk the dog", "Pay the bills", "Water the plants")
    todo_page.mark_completed("Pay the bills")

    todo_page.filter_by("Active")

    expect(todo_page.page).to_have_url(re.compile(r"#/active$"))
    expect(todo_page.todo_titles).to_have_text(["Walk the dog", "Water the plants"])
    expect(todo_page.item("Pay the bills")).to_have_count(0)


def test_completed_filter_shows_only_completed_items(todo_page):
    todo_page.add_todos("Walk the dog", "Pay the bills", "Water the plants")
    todo_page.mark_completed("Pay the bills")

    todo_page.filter_by("Completed")

    expect(todo_page.page).to_have_url(re.compile(r"#/completed$"))
    expect(todo_page.todo_titles).to_have_text(["Pay the bills"])
    expect(todo_page.item("Walk the dog")).to_have_count(0)
    expect(todo_page.item("Water the plants")).to_have_count(0)
