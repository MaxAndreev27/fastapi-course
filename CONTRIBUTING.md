# Contributing

## Getting Started

1. Fork the repository and create a branch from `main`.
2. Create and activate a Python 3.13 virtual environment.
3. Install dependencies with `pip install -r requirements.txt`.
4. Set `SECRET_KEY` and, if needed, `DATABASE_URL` in your environment or `.env` file.
5. Run migrations with `alembic upgrade head`.

## Development Workflow

1. Keep changes focused on one problem.
2. Add or update tests when behavior changes.
3. Run `pytest` before opening a pull request.
4. Describe the motivation and testing performed in the pull request template.

## Pull Requests

- Use a clear, descriptive title.
- Do not include unrelated formatting or generated-file changes.
- Ensure the GitHub Actions test workflow passes.
- Be respectful and follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Reporting Bugs and Requesting Features

Use the issue forms provided on GitHub. Include enough detail to reproduce a bug or evaluate a feature request.
