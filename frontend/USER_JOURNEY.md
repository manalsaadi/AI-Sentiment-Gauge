
# User Flow & User Journey (UX Standards)

This document defines polished UX user flows and journey maps for the AI-Powered Comment Analyzer. It follows UX industry best practices: clear goals, task-focused flows, success metrics, micro-interactions, error handling, accessibility requirements, and handoff notes for design and engineering.

**Goals:**
- **Primary:** Enable non-technical users to quickly analyze multilingual comments — detect language, translate to English, and get sentiment + keyword insights.
- **Secondary:** Provide exportable, shareable reports and a reliable scraping workflow for product discussions.

**Success Metrics (UX):**
- **Time to insight:** < 5s for small inputs (≤10 comments).
- **Task completion:** 90% of users can generate a report within 2 minutes.
- **Error recovery:** 95% of failures provide a clear next action (retry, upload, or configure selector).

## Personas (brief)
- **Marketer:** needs a fast sentiment snapshot from a pasted sample to make campaign decisions.
- **Product Manager:** needs to scrape discussion pages and extract top feature requests or bugs.

## UX Principles Applied
- **Clarity:** primary actions are visible and labelled with outcomes (e.g., `Analyze`, `Scrape & Analyze`).
- **Progressive Disclosure:** advanced options (selectors, headers, sample size) hidden behind `Advanced` to avoid overwhelming first-time users.
- **Immediate Feedback:** show step-level progress so users understand what is happening (Detect → Translate → Analyze).
- **Resilience:** degrade gracefully when offline resources (translation packages) are unavailable.
- **Accessibility:** keyboard-first navigation, ARIA roles for dynamic results, sufficient color contrast.

## Task Flows (UX-first, each includes goal, preconditions, steps, success criteria, edge cases)

- **Flow A — Paste Text (Quick Analysis)**
  - Goal: Get sentiment + keywords from pasted comments quickly.
  - Preconditions: User has a block of text (single or multiple comments).
  - Steps:
    1. User clicks `Paste Text` or focuses the dashboard textarea.
    2. User pastes comments; UI shows sample preview and line count.
    3. User confirms settings (Language: Auto, Target: English) and taps `Analyze`.
    4. UI shows stepper progress (Detecting → Translating → Analyzing) with spinner and a cancel link.
    5. Results render: sentiment chips, top keywords, and a paginated/comment table with filters.
  - Success criteria:
    - Results include `sentiment_distribution`, `top_keywords`, and a preview of translated text when source != English.
    - Visual focus lands on the sentiment summary for screen-reader users.
  - Edge cases & UX decisions:
    - Empty input: inline validation `Paste some text to analyze`.
    - Very long input: default to sampling first N lines with a clear `Analyze full text` option.

- **Flow B — Scrape URL (Fetch & Analyze)**
  - Goal: Scrape comments from a URL and analyze them.
  - Preconditions: User provides a reachable URL.
  - Steps:
    1. User opens `Scrape URL`, pastes the URL, optionally opens `Advanced` to provide CSS selector or User-Agent.
    2. User clicks `Scrape & Analyze`.
    3. UI shows live fetch log and stepper: Fetching → Extracting → Translating → Analyzing.
    4. UI progressively lists first N comments as they are found.
    5. Results render with a `Scrape report` that lists warnings and counts.
  - Success criteria:
    - User sees number of comments and can filter by language or sentiment.
    - Scrape report includes actionable warnings (e.g., `robots.txt blocked`, `Try a selector`).
  - Edge cases & UX decisions:
    - If scraping returns zero comments: show `No comments found` with examples and a `Try selector` CTA.
    - If robots.txt blocks scraping: show an explanation and `Upload HTML` alternative.

- **Flow C — Translate Quick Tool (Utility)**
  - Goal: Provide a fast translation check for a sentence.
  - Preconditions: User types a sentence into the header utility.
  - Steps:
    1. User opens Translate modal, types text.
    2. The app debounces detection (300ms) and shows `Detected: fr` for example.
    3. User taps `Translate` and sees translated text inline.
  - Success criteria:
    - Translated text and detected language shown; if translation unavailable, show `Translation not available — try analysis-only`.

- **Flow D — Export Report**
  - Goal: Create a sharable Markdown report of results.
  - Preconditions: User has analysis results in the session.
  - Steps:
    1. User clicks `Export` in Results view.
    2. Export modal shows toggles (Include original / include translations / include keyword counts).
    3. User clicks `Download Markdown`; a toast confirms success.
  - Success criteria:
    - Downloaded Markdown contains sentiment summary, top keywords, and sample original/translations.

## Interaction Patterns & Microcopy
- **Primary CTAs:** Use verbs with outcomes: `Analyze`, `Scrape & Analyze`, `Download Markdown`.
- **Progress copy:** Use step labels and short explanations: `Translating (2/5) — may take longer for large batches`.
- **Errors & recovery:** Short, action-oriented messages: `Translation unavailable. Retry or analyze without translation.`
- **Empty states:** Helpful tips and a primary action: `No comments yet — paste text or scrape a URL`.

## Accessibility & Internationalization
- Move focus to result summary after analysis; provide `aria-live` regions for progress updates.
- Ensure color contrast for sentiment chips; provide text labels for color-coded states.
- Support RTL locales and locale-aware number formatting in exports.

## Error Handling Patterns (UX)
- **Translation resources missing:** show a persistent yellow banner with `Translation unavailable — continue analysis (best-effort)` and an optional `Retry` button.
- **Scraping blocked:** show a modal explaining `Blocked by robots.txt` with alternatives: `Upload HTML`, `Try selector`.
- **Network timeout:** show a retry CTA and an estimated wait time message.

## Acceptance Criteria & QA Checklist (UX verifiable)
- **Flow A:** Paste Text produces a visible sentiment summary and top 5 keywords for a 10-line input.
- **Flow B:** Scrape URL returns a scrape count and a `Scrape report` for a known page with comments.
- **Flow C:** Translate modal shows detected language and translated text, or a clear `not available` state.
- **Export:** Generated Markdown contains the header summary and at least 3 example comment rows.

## Handoff Notes for Design & Engineering
- Provide component specs for: TextArea, StepperProgress, SentimentChips, KeywordTag, CommentTable (with filters), ExportModal.
- Annotate where to show warnings (top banner vs inline within results) and how cancellation should behave (soft-cancel: stop processing further items but keep current results).

---

This version focuses on UX standards: clear goals, measurable success criteria, task flows with edge cases, accessible interactions, microcopy examples, and handoff notes for implementation. If you'd like I can also:
- produce a compact UI component library mapping (component names + props), or
- create a lightweight clickable HTML prototype under `frontend/docs/` for quick stakeholder review.

## Prompt-Style UI Breakdown (Addendum)

Goal: A user wants to analyze comments from a URL and get translated, preprocessed, and analyzed results (sentiment + keywords) ready to export.

Screens:
- `Dashboard Screen` — entry point with primary CTAs: `Paste Text`, `Upload CSV`, `Scrape URL`, small Translate utility icon.
- `Paste Text Screen` — large textarea for pasted comments, language settings, and `Analyze` CTA.
- `Scrape URL Screen` — URL input, `Advanced` disclosure (CSS selector, User-Agent), `Scrape & Analyze` CTA, live progress log.
- `Progress Screen / Inline Progress Card` — compact stepper showing Detect → Translate → Analyze with cancel action and live log.
- `Results Screen` — sentiment summary, keyword list, comment table (Original / Detected / Translated / Sentiment), filters, Export button.
- `Translate Modal` — quick single-line translation utility with detected language chip and `Translate` CTA.
- `Export Modal` — toggles for including original/translations/keywords and `Download Markdown` CTA.

Key components (screen → components):
- Dashboard Screen:
  - `Primary CTA group`: Primary `Paste Text` button, secondary `Scrape URL` and `Upload CSV` buttons.
  - `Recent analyses card`: small list of previous reports with quick actions.
- Paste Text Screen:
  - `Multiline TextArea` with placeholder examples and line-count indicator.
  - `Language pill`: `Auto` / `Select language` dropdown.
  - `Target language dropdown`: defaults to `English`.
  - `Primary Analyze button`: prominent, labelled `Analyze`.
  - `Sample toggle`: `Analyze first N lines` for very long inputs.
- Scrape URL Screen:
  - `URL input` with validation.
  - `Advanced disclosure` containing `CSS selector` input and `User-Agent` field.
  - `Scrape & Analyze` primary button.
  - `Live fetch log`: streaming preview of the first N comments found.
- Progress Screen / Inline Progress Card:
  - `StepperProgress` with discrete step labels and status icons.
  - `Live log area` showing snippets as items are processed.
  - `Cancel` small-link to stop further processing.
- Results Screen:
  - `SentimentPie`: pie chart + large percentage chips (Positive / Neutral / Negative).
  - `KeywordTagList`: tag chips with counts and small sparkline or relative size.
  - `CommentTable`: columns Original | Detected | Translated | Sentiment, with filters and pagination.
  - `Export button`: top-right, opens `Export Modal`.
  - `Banner area`: for non-blocking warnings (translation unavailable, partial results).
- Translate Modal:
  - `SingleLineInput` with debounce detection (300ms) and `DetectedLanguageChip`.
  - `Translate CTA` and `Result area` showing `TranslatedText` and `Confidence` where available.
- Export Modal:
  - `ToggleIncludeOriginal`, `ToggleIncludeTranslations`, `ToggleIncludeKeywordCounts`.
  - `Filename input` and `Download Markdown` CTA.

Flow (navigation & interactions):
- From `Dashboard Screen`, clicking `Paste Text` navigates to `Paste Text Screen`.
- From `Dashboard Screen`, clicking `Scrape URL` opens `Scrape URL Screen` (or opens a modal on small screens).
- On `Paste Text Screen`, tapping `Analyze` replaces the CTA with an `Inline Progress Card`; when complete, the UI transitions to `Results Screen` with focus moved to `SentimentPie`.
- On `Scrape URL Screen`, tapping `Scrape & Analyze` opens the `Inline Progress Card` with live log; partial results appear and then `Results Screen` is rendered when done.
- Clicking the header `Translate` icon opens `Translate Modal`; completing translation closes modal and optionally copies translated text to clipboard.
- On `Results Screen`, clicking `Export` opens `Export Modal`; clicking `Download Markdown` starts a download and shows a success toast.

Microcopy examples (for UI):
- Analyze CTA: `Analyze` → subtext on hover: `Detect + Translate + Analyze comments`.
- Progress step text: `Translating (may take longer for many comments)`.
- Empty scrape state: `No comments found — try a CSS selector or upload HTML`.

Acceptance mapping (quick):
- If `Scrape URL` returns >0 comments, show `Results Screen` with comment count and sentiment chips.
- If translation packages are missing, show yellow `Translation unavailable — continue analysis (best-effort)` banner and proceed.

