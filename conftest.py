from collections.abc import Generator

import allure
import pytest
from playwright.sync_api import Page

from pages.todo_page import TodoPage
from tests.const import COMPLETED_TODOS, REQUIREMENTS, REQUIREMENTS_DOC, SEEDED_TODOS

DEFAULT_APP_URL = "https://demo.playwright.dev/todomvc/"


@pytest.fixture
def todo_page(page: Page, base_url: str | None) -> TodoPage:
    """A ``TodoPage`` opened on a clean application state.

    The application URL comes from the ``--base-url`` option (or the
    ``PYTEST_BASE_URL`` variable) and falls back to the public demo.
    pytest-playwright gives every test a fresh browser context, but the
    application persists todos in localStorage, so it is cleared explicitly
    rather than relying on context isolation.
    """
    todo = TodoPage(page, base_url or DEFAULT_APP_URL)
    todo.open()
    todo.clear_storage()
    return todo


@pytest.fixture
def case_id(request: pytest.FixtureRequest, browser_name: str) -> str:
    """The parametrize id of the current case without the browser prefix added by the plugin."""
    return request.node.callspec.id.removeprefix(f"{browser_name}-")


@pytest.fixture
def seeded_todos(todo_page: TodoPage) -> TodoPage:
    """A clean page pre-filled with ``SEEDED_TODOS``, with ``COMPLETED_TODOS`` marked completed."""
    todo_page.add_todos(*SEEDED_TODOS)
    for text in COMPLETED_TODOS:
        todo_page.mark_completed(text)
    return todo_page


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Turn ``@pytest.mark.covers("R1", ...)`` into Allure links to the requirements."""
    for item in items:
        for marker in item.iter_markers("covers"):
            for requirement_id in marker.args:
                if requirement_id not in REQUIREMENTS:
                    raise pytest.UsageError(
                        f"{item.nodeid}: unknown requirement {requirement_id!r} in @covers"
                    )
                item.add_marker(
                    allure.link(
                        f"{REQUIREMENTS_DOC}#{requirement_id.lower()}",
                        name=f"{requirement_id}: {REQUIREMENTS[requirement_id]}",
                        link_type="requirement",
                    )
                )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> Generator:
    """Attach a screenshot and the current URL to the Allure report of a failed test."""
    outcome = yield
    report = outcome.get_result()
    page = item.funcargs.get("page") if hasattr(item, "funcargs") else None
    if report.when == "call" and report.failed and page is not None and not page.is_closed():
        allure.attach(page.url, name="url", attachment_type=allure.attachment_type.URI_LIST)
        allure.attach(
            page.screenshot(full_page=True),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
