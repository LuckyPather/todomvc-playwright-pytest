"""Marking a todo item as completed."""

from playwright.sync_api import expect

from pages.todo_page import TodoPage


def test_completed_item_appears_in_completed_view(todo_page: TodoPage) -> None:
    todo_page.add_todos("Write the report", "Review pull requests")
    report = todo_page.item("Write the report")

    todo_page.mark_completed("Write the report")

    expect(report).to_have_class("completed")
    expect(report.get_by_role("checkbox")).to_be_checked()
    expect(todo_page.items_left_counter).to_have_text("1 item left")

    todo_page.filter_by("Completed")
    expect(todo_page.todo_titles).to_have_text(["Write the report"])
    expect(report.get_by_role("checkbox")).to_be_checked()
