# Pre-commit Setup

This project uses pre-commit hooks to ensure code quality and consistency. The hooks are defined in the `.pre-commit-config.yaml` file and are run automatically before each commit.

## Setup

The pre-commit hooks are already installed in your Git repository. If you need to reinstall them:

```bash
pre-commit install
```

## Available Hooks

The following hooks are configured:

- **pre-commit-hooks**: Basic file checks (trailing whitespace, file endings, etc.)
- **black**: Python code formatter
- **ruff**: Fast Python linter
- **mypy**: Static type checker
- **isort**: Import sorter
- **pyupgrade**: Automatically upgrade Python syntax
- **tox-ini-fmt**: Tox.ini formatter

## Running Hooks Manually

You can run the hooks manually on all files:

```bash
pre-commit run --all-files
```

Or on specific files:

```bash
pre-commit run --files <file1> <file2>
```

## Integration with tox

You can run the pre-commit hooks through tox:

```bash
tox -e lint
```

This is useful for CI/CD pipelines or for checking code quality before making a PR.

## Skipping Hooks

In rare cases, you may need to skip hooks for a specific commit:

```bash
git commit --no-verify
```

But this should be avoided unless absolutely necessary.
