# TodoMVC UI tests

[![tests](https://github.com/LuckyPather/todomvc-playwright-pytest/actions/workflows/tests.yml/badge.svg)](https://github.com/LuckyPather/todomvc-playwright-pytest/actions/workflows/tests.yml)

Automated end-to-end tests for the [TodoMVC demo application](https://demo.playwright.dev/todomvc/),
built with Playwright for Python and pytest.

## Requirements coverage

| # | Requirement | Covered by |
|---|-------------|------------|
| 1 | A new todo item can be added using English text | `tests/test_adding.py::test_new_todo_item_is_added` — case `english-text` |
| 2 | A new todo item can be added using non-English characters | `tests/test_adding.py::test_new_todo_item_is_added` — cases `cyrillic`, `japanese`, `arabic-rtl`, `diacritics`, `emoji` |
| 3 | A new todo item can be added that includes numbers | `tests/test_adding.py::test_new_todo_item_is_added` — cases `text-with-numbers`, `digits-only`, `special-characters` |
| 4 | A todo item can be marked as completed and appears correctly in the "Completed" view | `tests/test_completing.py::test_completed_item_appears_in_completed_view` |
| 5 | A todo item can be deleted and no longer appears in any view | `tests/test_deleting.py::test_deleted_item_disappears_from_every_view` — checks the All, Active and Completed views, for both an active and a completed item |
| 6 | The "Active" filter correctly shows only items that are not completed | `tests/test_filtering.py::test_active_filter_shows_only_active_items` |
| 7 | The "Completed" filter correctly shows only items that have been marked as completed | `tests/test_filtering.py::test_completed_filter_shows_only_completed_items` |

## Getting started

Prerequisites: Python 3.12 or newer.

```
git clone https://github.com/LuckyPather/todomvc-playwright-pytest.git
cd todomvc-playwright-pytest

# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
playwright install chromium
```

On Linux, install the browser together with its system dependencies:
`playwright install --with-deps chromium`.

Run the suite:

```
pytest
```

## Other ways to run

| Purpose | Command |
|---------|---------|
| Watch the browser (headed mode) | `pytest --headed` |
| Different browser | `pytest --browser firefox` (run `playwright install firefox` once) |
| Parallel run | `pytest -n auto` |
| Smoke subset (one scenario per area) | `pytest -m smoke` |
| One functional area | `pytest -m filtering` (also `adding`, `completing`, `deleting`) |
| One parametrized case | `pytest -k cyrillic` |
| Slow motion for debugging | `pytest --headed --slowmo 300` |
| Verbose test names | `pytest -v` |

Markers are registered in `pyproject.toml` and enforced with `--strict-markers`; run
`pytest --markers` to list them.

When a test fails, a screenshot and a Playwright trace are saved under `test-results/`.
Open a trace with `playwright show-trace <path-to-trace.zip>`.

## Project structure

```
conftest.py            fixture: page object on a clean application state
pages/todo_page.py     page object: locators, user actions and filter routes for TodoMVC
tests/                 one file per functional area, assertions via expect()
pyproject.toml         pytest, ruff and black configuration
requirements*.txt      pinned runtime and development dependencies
.github/workflows/     CI pipeline
```

## Design decisions

- **Page object** (`pages/todo_page.py`) holds locators and user actions in one place, so tests
  read as user scenarios. Assertions stay in the tests and use Playwright's auto-waiting
  `expect()` — no sleeps or manual retries anywhere.
- **Semantic locators only**: placeholder text, `data-testid` attributes, ARIA roles and labels.
  No XPath or positional CSS chains, so tests survive markup changes.
- **Clean state per test**: every test gets a fresh browser context, and the `todo_page` fixture
  additionally clears `localStorage`, where the application persists todos. Tests are independent,
  order-agnostic and safe to run in parallel.
- **Parametrization** covers all three "add" requirements in a single test with readable case ids
  instead of near-identical copies; the data set spans Cyrillic, Japanese, Arabic (right-to-left),
  diacritics, emoji and HTML-sensitive special characters.
- **Deletion is verified in all three views** (All, Active, Completed), matching the literal
  wording of the requirement, and for both an active and a completed item.
- **Scope is limited to the seven required scenarios.** Adjacent features (editing, mark all as
  complete, clearing completed, persistence across reloads) are deliberately out of scope.

## Development

Linting and formatting are enforced with ruff and black:

```
pip install -r requirements-dev.txt
ruff check .
black --check .
```

## Continuous integration

GitHub Actions ([tests.yml](.github/workflows/tests.yml)) runs two jobs on every push and pull
request: `lint` (ruff and black) and `test` (the suite, headless with Chromium, in parallel).
For a failed run, screenshots and traces are attached to the run as the `test-artifacts`
artifact.
