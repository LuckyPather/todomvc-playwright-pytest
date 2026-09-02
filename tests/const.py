"""Constants shared by the tests."""

REQUIREMENTS_DOC = (
    "https://github.com/LuckyPather/todomvc-playwright-pytest/blob/main/docs/requirements.md"
)

# Requirement id -> title, as described in docs/requirements.md (anchors match the lowercase id).
REQUIREMENTS = {
    "R1": "A new todo item can be added using English text",
    "R2": "A new todo item can be added using non-English characters",
    "R3": "A new todo item can be added that includes numbers",
    "R4": 'A todo item can be marked as completed and appears in the "Completed" view',
    "R5": "A todo item can be deleted and no longer appears in any view",
    "R6": 'The "Active" filter shows only items that are not completed',
    "R7": 'The "Completed" filter shows only items that have been marked as completed',
}

# Todos entered by the seeded_todos fixture, in insertion order, and the ones it marks completed.
SEEDED_TODOS = ("Walk the dog", "Pay the bills", "Water the plants")
COMPLETED_TODOS = ("Pay the bills",)
ACTIVE_TODOS = tuple(text for text in SEEDED_TODOS if text not in COMPLETED_TODOS)
