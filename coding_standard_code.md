# Coding Standards for AI-Powered Comment Analyzer

These coding standards ensure code quality, maintainability, and readability across the project. They apply to all Python code written for the analyzer, including modules for scraping, preprocessing, translation, analysis, and reporting.

---

## 1. General Principles
- Write **clear, maintainable, and well-structured code**.
- Strive for **simplicity**; avoid over-engineering.
- Follow the principle of **Separation of Concerns**: scraping, translation, preprocessing, analysis, and reporting must be modular.
- Ensure the code runs entirely **locally** with no hidden external dependencies.

---

## 2. Python Coding Style
- Follow **PEP 8** as the base style guide.
- Use **4 spaces** for indentation, never tabs.
- Keep line length ≤ **100 characters**.
- Use **meaningful variable and function names**:
  - `good`: `extract_comments_from_html()`
  - `bad`: `foo()` or `process1()`
- Use **snake_case** for functions and variables, **PascalCase** for classes, **UPPER_CASE** for constants.
- Avoid deeply nested code; refactor into helper functions or classes.

---

## 3. Documentation & Comments
- Every public function and class must have a **docstring** (PEP 257).
- Use Google-style or NumPy-style docstrings consistently.
- Inline comments only when logic is non-obvious.
- Module top: short description of purpose.

---

## 4. Type Hints
- Use **Python type hints** everywhere.
- Run `mypy` type checker before commit.

---

## 5. Project Structure
- /project_root
- /src
- /input # CLI and scraping
- /translation # Language detection & offline translation
- /preprocessing # Cleaning and normalization
- /analysis # Sentiment + keyword extraction
- /reporting # Markdown, JSON, visualizations
- /tests
requirements.txt
README.md
.gitignore


---

## 6. Testing Standards
- Use **pytest**.
- Write failing test first → code → refactor.
- Test coverage target: **≥80%**.
- Include positive, negative, edge, and performance tests.
- Incorporate **industry standard multilingual test datasets** for validation.
- Include **performance tests benchmarking 500 comments processed within 15 seconds**.

---

## 7. Error Handling
- Fail gracefully with meaningful error messages.
- Log or raise exceptions—never silent fail.

---

## 8. Logging Standards
- Use `logging` module, not `print()`.
- Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL.

---

## 9. Dependency Management
- Pin versions in `requirements.txt`.
- Avoid heavy libraries unless justified.
- Argos Translate chosen for **V1 offline translation** integration, MarianMT reserved for **V2 upgrade**.
- Test upgrades regularly.

---

## 10. Security & Compliance
- Scraper **must respect `robots.txt`**.
- No cloud APIs or external services for translation or analysis.
- GDPR compliance: no uploading of user data externally.
- Raw comment data should not be saved without explicit user consent.

---

## 11. Performance
- Must handle **at least 5,000 comments** without memory issues.
- Batch process translation and analysis for efficiency.
- V1 supports basic sentiment categories only; extension for intensity scoring planned for V2.
- Keyword extraction to implement **both frequency-based and TF-IDF** from the start.

---

## 12. Input Handling and Analysis
- Support **both single comment and batch input** for paste functionality.
- Prioritize **social media and e-commerce product comments** for web scraping in V1.
- Sentiment analysis to start with basic categories (positive, negative, neutral) in V1.
- Plan to add sentiment **intensity (e.g., very positive)** in V2.

---

## 13. Output Formats
- Markdown reports implemented in V1.
- JSON reports planned for V2.
- CSV export deferred beyond V2.

---

## 14. Version Control
- Use **Git** with meaningful commit messages (`feat:`, `fix:`, `test:`, etc.).
- Protect `main` branch with reviews and PRs before merging.

---

## 15. Style & Quality Tools
- Use `flake8` for linting.
- Use `black` for auto-formatting.
- Use `isort` for import sorting.
- Use `pytest` with coverage plugin for testing.
- Use `mypy` for type checking.

---

## 16. Code Review Guidelines
- Each PR reviewed by at least one developer.
- Reviewer checks for:
  - Compliance with code standards.
  - Available and passing tests.
  - Proper error handling and logging.
  - Use of Argos Translate for translation in V1.
  
---

## 17. Documentation Standards
- Maintain comprehensive README including:
  - Supported languages: **English, French, German, Spanish** initially.
  - Use Argos Translate for offline translation in V1, plan MarianMT for V2.
  - Input methods: paste (single & batch), web scraping (social media and e-commerce).
  - Output: Markdown reports with sentiment and keyword summaries.
  - Roadmap to V2 features.
- Docstrings must explain *what* the code does and *why*.
