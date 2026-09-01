"""Page object for the TodoMVC demo application."""

from playwright.sync_api import Locator, Page

APP_URL = "https://demo.playwright.dev/todomvc/"


class TodoPage:
    """Encapsulates locators and user actions for the TodoMVC page.

    The page object exposes locators and actions only; assertions live in the
    tests, built on Playwright's auto-waiting ``expect()``.
    """

    def __init__(self, page: Page) -> None:
        self.page = page
        self.new_todo_input = page.get_by_placeholder("What needs to be done?")
        self.todo_items = page.get_by_test_id("todo-item")
        self.todo_titles = page.get_by_test_id("todo-title")
        self.items_left_counter = page.get_by_test_id("todo-count")

    def open(self) -> None:
        self.page.goto(APP_URL)

    def clear_storage(self) -> None:
        """Remove persisted todos so every test starts from a clean slate."""
        self.page.evaluate("localStorage.clear()")
        self.page.reload()

    def add_todo(self, text: str) -> None:
        self.new_todo_input.fill(text)
        self.new_todo_input.press("Enter")

    def add_todos(self, *texts: str) -> None:
        for text in texts:
            self.add_todo(text)

    def item(self, text: str) -> Locator:
        return self.todo_items.filter(has_text=text)

    def mark_completed(self, text: str) -> None:
        self.item(text).get_by_role("checkbox").check()

    def delete(self, text: str) -> None:
        item = self.item(text)
        item.hover()
        item.get_by_role("button", name="Delete").click()

    def filter_by(self, name: str) -> None:
        """Switch the current view. ``name`` is one of All, Active, Completed."""
        self.page.get_by_role("link", name=name, exact=True).click()
