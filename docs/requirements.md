# Requirements

Functional requirements of the [TodoMVC demo application](https://demo.playwright.dev/todomvc/)
verified by this suite. Every test links to the requirement it covers in the Allure report,
and the README maps each requirement to its test.

<a id="r1"></a>
## R1. A new todo item can be added using English text

Acceptance: after the text is entered and confirmed with Enter, the item is listed with exactly
that text, the counter reads "1 item left" and the input field is cleared.

<a id="r2"></a>
## R2. A new todo item can be added using non-English characters

Acceptance: as R1, for text in other scripts and writing directions (Cyrillic, Japanese,
right-to-left Arabic, Latin with diacritics, emoji).

<a id="r3"></a>
## R3. A new todo item can be added that includes numbers

Acceptance: as R1, for text that contains digits, for digits only, and for digits mixed with
punctuation and symbols.

<a id="r4"></a>
## R4. A todo item can be marked as completed and appears correctly in the "Completed" view

Acceptance: after the checkbox of an item is ticked, the item is rendered as completed, its
checkbox stays checked, the counter no longer counts it, and the "Completed" view lists that
item and nothing else.

<a id="r5"></a>
## R5. A todo item can be deleted and no longer appears in any view

Acceptance: after the delete button of an item is clicked, the item is absent from the "All",
"Active" and "Completed" views, the counter is updated, and the other items remain. This holds
for an active item and for a completed one.

<a id="r6"></a>
## R6. The "Active" filter correctly shows only items that are not completed

Acceptance: with a mix of active and completed items, the "Active" view lists every active item
in insertion order and no completed item.

<a id="r7"></a>
## R7. The "Completed" filter correctly shows only items that have been marked as completed

Acceptance: with a mix of active and completed items, the "Completed" view lists every completed
item in insertion order and no active item.
