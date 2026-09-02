"""Page object for the TodoMVC demo application."""

from typing import Literal

import allure
from playwright.sync_api import Locator, Page

FilterName = Literal["All", "Active", "Completed"]

# Hash route the application navigates to when a filter link is clicked.
FILTER_ROUTES: dict[FilterName, str] = {
    "All": r"#/$",
    "Active": r"#/active$",
    "Completed": r"#/completed$",
}


class TodoPage:
    """Encapsulates locators and user actions for the TodoMVC page.

    The page object exposes locators and actions only; assertions live in the
    tests, built on Playwright's auto-waiting ``expect()``. Every action is an
    Allure step, so reports show the scenario as the user performed it.
    """

    def __init__(self, page: Page, url: str) -> None:
        self.page = page
        self.url = url
        self.new_todo_input = page.get_by_placeholder("What needs to be done?")
        self.todo_items = page.get_by_test_id("todo-item")
        self.todo_titles = page.get_by_test_id("todo-title")
        self.items_left_counter = page.get_by_test_id("todo-count")

    @allure.step("Open the application")
    def open(self) -> None:
        self.page.goto(self.url)

    @allure.step("Clear persisted todos")
    def clear_storage(self) -> None:
        """Remove persisted todos so every test starts from a clean slate."""
        self.page.evaluate("localStorage.clear()")
        self.page.reload()

    @allure.step("Add todo {text}")
    def add_todo(self, text: str) -> None:
        self.new_todo_input.fill(text)
        self.new_todo_input.press("Enter")

    def add_todos(self, *texts: str) -> None:
        for text in texts:
            self.add_todo(text)

    def item(self, text: str) -> Locator:
        """The todo item whose title is exactly ``text``."""
        return self.todo_items.filter(has=self.page.get_by_text(text, exact=True))

    @allure.step("Mark {text} as completed")
    def mark_completed(self, text: str) -> None:
        self.item(text).get_by_role("checkbox").check()

    @allure.step("Delete {text}")
    def delete(self, text: str) -> None:
        item = self.item(text)
        item.hover()
        item.get_by_role("button", name="Delete").click()

    @allure.step("Switch to the {name} view")
    def filter_by(self, name: FilterName) -> None:
        """Switch the current view by clicking one of the footer filter links."""
        self.page.get_by_role("link", name=name, exact=True).click()
