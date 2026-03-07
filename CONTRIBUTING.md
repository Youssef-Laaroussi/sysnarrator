# Contributing to SysNarrator

Thank you for your interest in contributing! 🎉  
SysNarrator is a community project and every contribution matters.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Adding a Language](#adding-a-language)
- [Reporting Bugs](#reporting-bugs)

---

## Code of Conduct

Be respectful. Be kind. We are all here to build something useful together.  
Harassment, discrimination, or toxic behavior will not be tolerated.

---

## How to Contribute

### 🐛 Found a bug?
Open an issue using the **Bug Report** template.  
Include your OS version, Python version, and steps to reproduce.

### 💡 Have a feature idea?
Open an issue using the **Feature Request** template.  
Describe the problem it solves, not just the solution.

### 🌍 Want to translate?
See the [Adding a Language](#adding-a-language) section below.

### 💻 Want to write code?
1. Look for issues labeled `good first issue` or `help wanted`
2. Comment on the issue to claim it
3. Fork, code, test, PR!

---

## Development Setup

```bash
# 1. Fork the repo on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/sysnarrator.git
cd sysnarrator

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install in dev mode with all dependencies
pip install -e ".[dev]"

# 4. Run tests to make sure everything works
pytest

# 5. Create your branch
git checkout -b feature/my-feature
```

---

## Coding Standards

- **Python 3.10+** — Use type hints where practical
- **PEP 8** — Run `flake8` before committing
- **Docstrings** — Add docstrings to all public functions
- **Tests** — Add tests for any new functionality
- **No new dependencies** — Unless absolutely necessary (discuss in issue first)

```bash
# Check formatting
flake8 sysnarrator/

# Run tests
pytest tests/ -v

# Check test coverage
pytest --cov=sysnarrator tests/
```

---

## Submitting a Pull Request

1. Make sure all tests pass: `pytest`
2. Update `CHANGELOG.md` with your changes under `[Unreleased]`
3. Push your branch and open a PR against `main`
4. Fill out the PR template completely
5. Wait for review — we usually respond within 48h

**PR title format:** `feat: add discord webhook alerts` or `fix: cpu percent on ARM`

---

## Adding a Language

1. Copy `sysnarrator/i18n/en.json`
2. Rename it to your language code (e.g., `es.json` for Spanish)
3. Translate all values (keep the keys in English!)
4. Add your language to the table in `README.md`
5. Open a PR with title `i18n: add Spanish (es)`

Example `i18n/en.json` structure:
```json
{
  "cpu": {
    "critical": "CPU saturated at {pct}% — system is under extreme pressure.",
    "warning": "CPU loaded at {pct}% — performance starting to degrade.",
    "ok": "CPU quiet at {pct}% — your machine is breathing easy."
  },
  ...
}
```

---

## Reporting Bugs

Please include:
- **OS and version** (e.g., Ubuntu 24.04)
- **Python version** (`python3 --version`)
- **SysNarrator version** (`sysnarrator --version`)
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Error output** (full traceback if available)

---

Thank you for making SysNarrator better! 💙
