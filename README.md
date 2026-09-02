# TodoMVC UI tests

[![tests](https://github.com/LuckyPather/todomvc-playwright-pytest/actions/workflows/tests.yml/badge.svg)](https://github.com/LuckyPather/todomvc-playwright-pytest/actions/workflows/tests.yml)

Automated end-to-end tests for the [TodoMVC demo application](https://demo.playwright.dev/todomvc/),
built with Playwright for Python and pytest.

## Requirements coverage

The requirements, with their acceptance criteria, are described in
[docs/requirements.md](docs/requirements.md); each test links to the ones it verifies.

| # | Requirement | Covered by |
|---|-------------|------------|
| 1 | A new todo item can be added using English text | `tests/test_adding.py::test_new_todo_item_is_added` — case `english-text` |
| 2 | A new todo item can be added using non-English characters | `tests/test_adding.py::test_new_todo_item_is_added` — cases `cyrillic`, `japanese`, `arabic-rtl`, `diacritics`, `emoji` |
| 3 | A new todo item can be added that includes numbers | `tests/test_adding.py::test_new_todo_item_is_added` — cases `text-with-numbers`, `digits-only`, `special-characters` |
| 4 | A todo item can be marked as completed and appears correctly in the "Completed" view | `tests/test_completing.py::test_completed_item_appears_in_completed_view` |
| 5 | A todo item can be deleted and no longer appears in any view | `tests/test_deleting.py::test_deleted_item_disappears_from_every_view` — checks the All, Active and Completed views, for both an active and a completed item |
| 6 | The "Active" filter correctly shows only items that are not completed | `tests/test_filtering.py::test_active_filter_shows_only_active_items` |
| 7 | The "Completed" filter correctly shows only items that have been marked as completed | `tests/test_filtering.py::test_completed_filter_shows_only_completed_items` |

### Beyond the requirements

Boundary and negative scenarios around the required flows are marked `edge` (run or skip them
with `-m edge` / `-m "not edge"`). They pin down behaviour that was verified against the live
application first:

| Scenario | Covered by |
|----------|------------|
| Single character, very long text, HTML markup shown as plain text | `test_new_todo_item_is_added` — cases `single-character`, `long-text`, `html-markup` |
| Surrounding whitespace is trimmed | `test_surrounding_whitespace_is_trimmed` |
| Empty or whitespace-only input adds nothing | `test_blank_input_does_not_add_an_item` — cases `empty`, `whitespace-only` |
| Identical items can coexist | `test_duplicate_items_are_allowed` |
| Deleting the only item leaves an empty list without a footer | `test_deleting_the_only_item_leaves_an_empty_list` |
| Active filter is empty when everything is completed (counter reads "0 items left") | `test_active_filter_is_empty_when_every_item_is_completed` |
| Completed filter is empty when nothing is completed | `test_completed_filter_is_empty_when_nothing_is_completed` |

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
| Smoke subset (at least one scenario per area) | `pytest -m smoke` |
| Core requirements only, without edge cases | `pytest -m "not edge"` |
| One functional area | `pytest -m filtering` (also `adding`, `completing`, `deleting`) |
| One parametrized case | `pytest -k cyrillic` |
| Slow motion for debugging | `pytest --headed --slowmo 300` |
| Another deployment of the application | `pytest --base-url http://localhost:8080/` (or set `PYTEST_BASE_URL`) |

Markers are registered in `pyproject.toml` and enforced with `--strict-markers`; run
`pytest --markers` to list them.

When a test fails, a screenshot and a Playwright trace are saved under `test-results/`.
Open a trace with `playwright show-trace <path-to-trace.zip>`.

## Reports

Every run writes Allure results to `allure-results/`. To browse them locally, install the
[Allure command line](https://allurereport.org/docs/install/) and run:

```
allure serve allure-results
```

The report of the latest `main` build is published to GitHub Pages:
https://luckypather.github.io/todomvc-playwright-pytest/.

Each test is annotated for the report with a readable title (built at run time for parametrized
cases), a description, a severity, a stable id and links to the requirements it covers; page
object actions and assertion groups are recorded as steps. Failed tests carry a screenshot and
the page URL as attachments, and pytest markers appear as tags.

## Project structure

```
conftest.py            fixtures (clean page, seeded todo list, case id), default application URL, Allure failure hook
pages/todo_page.py     page object: locators, user actions (recorded as Allure steps) and filter routes
tests/requirements.py  the requirements as data, plus the decorator that links a test to them
tests/seeds.py         shared test data: a seeded list with active and completed items
tests/test_*.py        one file per functional area, assertions via expect()
docs/requirements.md   the requirements with acceptance criteria
pyproject.toml         pytest, ruff and black configuration
requirements*.txt      pinned runtime and development dependencies
.github/workflows/     CI pipeline
```

## Design decisions

- **Page object** (`pages/todo_page.py`) holds locators and user actions in one place, so tests
  read as user scenarios. Assertions stay in the tests and use Playwright's auto-waiting
  `expect()` — no sleeps or manual retries anywhere.
- **Semantic locators only**: placeholder text, `data-testid` attributes, ARIA roles with their
  accessible names, and exact visible text. No XPath or positional CSS chains, so tests survive
  markup changes.
- **Clean state per test**: every test gets a fresh browser context, and the `todo_page` fixture
  additionally clears `localStorage`, where the application persists todos. Tests are independent,
  order-agnostic and safe to run in parallel.
- **Parametrization** covers all three "add" requirements in a single test with readable case ids
  instead of near-identical copies; the data set spans Cyrillic, Japanese, Arabic (right-to-left),
  diacritics, emoji and HTML-sensitive special characters.
- **Deletion is verified in all three views** (All, Active, Completed), matching the literal
  wording of the requirement, and for both an active and a completed item.
- **Shared setup lives in fixtures, not in tests.** Scenarios that start from "a list with one
  completed item" use the `seeded_todos` fixture, which returns the seeded data alongside the
  page, so expected values are derived from the same source as the setup. Scenarios where the
  setup is the subject of the test (adding, completing) keep it inline for readability.
- **Plain test functions, no test classes.** Grouping is done by module and by pytest markers,
  which is all that a suite without shared mutable state needs.
- **Scope stays around the seven required flows.** Edge cases cover boundaries of those flows;
  adjacent features (editing, mark all as complete, clearing completed, persistence across
  reloads) are deliberately out of scope.

## Development

Linting and formatting are enforced with ruff and black:

```
pip install -r requirements-dev.txt
ruff check .
black --check .
```

## Continuous integration

GitHub Actions ([tests.yml](.github/workflows/tests.yml)) runs on every push and pull request:

- `lint`: ruff and black.
- `test`: the suite, headless with Chromium, in parallel. Allure results are always uploaded as
  the `allure-results` artifact; for a failed run, screenshots and traces are added as
  `test-artifacts`.
- `report` (pushes to `main` only): generates the Allure report and deploys it to GitHub Pages.
