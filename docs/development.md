---
icon: lucide/code
---

# Development Guide

This guide covers everything you need to know to develop, test, and contribute to the FastAPI Backend Template.

## 🛠️ Local Environment Setup

### 1. Install `uv`
This project uses `uv` for lightning-fast dependency management.
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Sync Dependencies
```bash
uv sync
```

### 3. Pre-commit Hooks
Install pre-commit hooks to ensure code quality:
```bash
uv run pre-commit install
```

## 🚀 Running the API Locally

### Start Development Server
```bash
uv run fastapi dev
```
The server will start with hot-reload enabled at http://localhost:8000.

## 🧪 Testing

We use **Pytest** for our testing suite.

### Run All Tests
```bash
uv run pytest
```

### Run with Coverage
```bash
uv run pytest --cov=app --cov-report=term-missing
```

## 🧹 Linting & Formatting

We use **Ruff** for linting and formatting.

### Run Linter
```bash
uv run ruff check .
```

### Fix Linting Errors
```bash
uv run ruff check --fix .
```

### Run Formatter
```bash
uv run ruff format .
```

## 🔍 Type Checking

We use **Mypy** for static type checking.
```bash
uv run mypy .
```

## 🤖 Gemini CLI

This project is optimized for AI-driven development.
```bash
# Research and modify
gemini "Add a new endpoint to list users"
```
Refer to `GEMINI.md` for project-specific AI mandates.
